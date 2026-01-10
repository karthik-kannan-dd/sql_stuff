from datetime import date

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from delivery_queries import (
    get_delivery_details,
    get_store_wait_comparison,
    get_store_historical_stats,
    compute_comparison_stats,
)

st.set_page_config(
    page_title="Delivery Store Wait Analysis",
    page_icon="stopwatch",
    layout="wide",
)

st.title("Delivery Store Wait Analysis")
st.markdown(
    "Compare a delivery's store wait time against other dashers at the same store. "
    "Based on the methodology from the Tier 2 deep dive analysis."
)

# Sidebar inputs
st.sidebar.header("Parameters")

delivery_id = st.sidebar.number_input(
    "Delivery ID",
    min_value=1,
    value=None,
    placeholder="Enter Delivery ID",
    help="Enter the delivery ID to analyze",
)

st.sidebar.subheader("Date Bounds")
start_date = st.sidebar.date_input(
    "Start Date",
    value=date(2025, 12, 10),
    help="Lower bound for delivery date range",
)

end_date = st.sidebar.date_input(
    "End Date",
    value=date(2026, 1, 7),
    help="Upper bound for delivery date range",
)

st.sidebar.subheader("Store Comparison")
lookback_days = st.sidebar.slider(
    "Store History Lookback (days)",
    min_value=7,
    max_value=90,
    value=28,
    help="Days to look back from the delivery date for store comparison",
)

if st.sidebar.button("Analyze", type="primary") or delivery_id:
    if not delivery_id:
        st.warning("Please enter a Delivery ID")
    else:
        with st.spinner("Fetching delivery data from Snowflake..."):
            try:
                delivery = get_delivery_details(delivery_id, start_date, end_date)

                if delivery is None:
                    st.error(f"No data found for Delivery {delivery_id}")
                else:
                    # Delivery details section
                    st.header("Delivery Details")

                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Delivery ID", int(delivery["delivery_id"]))
                    with col2:
                        st.metric("Dasher ID", int(delivery["dasher_id"]))
                    with col3:
                        st.metric("Store", delivery["store_name"][:30] if delivery["store_name"] else "N/A")
                    with col4:
                        st.metric("Pay Model", delivery["timebased_pay_model"] or "N/A")

                    col5, col6, col7, col8 = st.columns(4)
                    with col5:
                        wait = delivery["wait_time_min"]
                        st.metric("Store Wait Time", f"{wait:.1f} min" if wait else "N/A")
                    with col6:
                        st.metric("Pickup Lateness", f"{delivery['pickup_late_min']:.1f} min")
                    with col7:
                        st.metric("Dropoff Lateness", f"{delivery['dropoff_late_min']:.1f} min")
                    with col8:
                        st.metric("Total Lateness", f"{delivery['total_late_min']:.1f} min")

                    arrival_time = delivery.get("store_arrival_time")
                    if arrival_time:
                        st.info(f"**Store Arrival Time:** {arrival_time}")

                    st.divider()

                    # Store comparison section
                    if delivery["store_id"] and arrival_time and delivery["wait_time_min"]:
                        st.header("Store Wait Time Comparison")
                        st.markdown(
                            f"Comparing this dasher's **{delivery['wait_time_min']:.1f} min** wait "
                            f"against other dashers at **{delivery['store_name']}** who arrived within 60 minutes before."
                        )

                        with st.spinner("Fetching comparison data..."):
                            comparison_df = get_store_wait_comparison(
                                store_id=delivery["store_id"],
                                store_arrival_time=str(arrival_time),
                                dasher_id=delivery["dasher_id"],
                                lookback_days=lookback_days,
                            )

                            stats = compute_comparison_stats(comparison_df, delivery["wait_time_min"])

                            # Comparison metrics
                            st.subheader("Lookback Window Comparison")
                            col_a, col_b, col_c = st.columns(3)

                            with col_a:
                                if stats["n_10m"] > 0:
                                    gap_10 = delivery["wait_time_min"] - stats["avg_10m"]
                                    st.metric(
                                        "10-min Window",
                                        f"{stats['avg_10m']:.1f} min avg",
                                        delta=f"{gap_10:+.1f} min gap",
                                        delta_color="inverse",
                                    )
                                    st.caption(f"n={stats['n_10m']} dashers")
                                else:
                                    st.metric("10-min Window", "No data")
                                    st.caption("No other dashers in window")

                            with col_b:
                                if stats["n_30m"] > 0:
                                    gap_30 = delivery["wait_time_min"] - stats["avg_30m"]
                                    st.metric(
                                        "30-min Window",
                                        f"{stats['avg_30m']:.1f} min avg",
                                        delta=f"{gap_30:+.1f} min gap",
                                        delta_color="inverse",
                                    )
                                    st.caption(f"n={stats['n_30m']} dashers")
                                else:
                                    st.metric("30-min Window", "No data")
                                    st.caption("No other dashers in window")

                            with col_c:
                                if stats["n_60m"] > 0:
                                    gap_60 = delivery["wait_time_min"] - stats["avg_60m"]
                                    st.metric(
                                        "60-min Window",
                                        f"{stats['avg_60m']:.1f} min avg",
                                        delta=f"{gap_60:+.1f} min gap",
                                        delta_color="inverse",
                                    )
                                    st.caption(f"n={stats['n_60m']} dashers")
                                else:
                                    st.metric("60-min Window", "No data")
                                    st.caption("No other dashers in window")

                            # Interpretation
                            if stats["n_60m"] > 0 and stats["avg_60m"]:
                                ratio = delivery["wait_time_min"] / stats["avg_60m"]
                                gap = delivery["wait_time_min"] - stats["avg_60m"]

                                if ratio >= 3:
                                    st.error(
                                        f"This dasher waited **{ratio:.1f}x longer** than peers "
                                        f"(+{gap:.1f} min). Store slowness claim is **not supported**."
                                    )
                                elif ratio >= 2:
                                    st.warning(
                                        f"This dasher waited **{ratio:.1f}x longer** than peers "
                                        f"(+{gap:.1f} min). Elevated wait time."
                                    )
                                elif ratio >= 1.5:
                                    st.info(
                                        f"This dasher waited **{ratio:.1f}x longer** than peers "
                                        f"(+{gap:.1f} min). Moderately above average."
                                    )
                                else:
                                    st.success(
                                        f"This dasher's wait time is within normal range for this store "
                                        f"({ratio:.1f}x peers, {gap:+.1f} min)."
                                    )
                            elif stats["n_60m"] == 0:
                                st.warning("No comparison data available - no other dashers at this store in the 60-min window.")

                            st.divider()

                            # Visualization
                            if not comparison_df.empty:
                                st.subheader("Wait Time Distribution")

                                chart_col1, chart_col2 = st.columns(2)

                                with chart_col1:
                                    # Histogram of other dashers' wait times
                                    fig_hist = px.histogram(
                                        comparison_df,
                                        x="wait_time_min",
                                        nbins=20,
                                        title="Other Dashers' Wait Times (60-min window)",
                                        labels={"wait_time_min": "Wait Time (min)", "count": "Count"},
                                    )
                                    fig_hist.add_vline(
                                        x=delivery["wait_time_min"],
                                        line_dash="dash",
                                        line_color="red",
                                        annotation_text=f"This Dasher ({delivery['wait_time_min']:.1f})",
                                    )
                                    if stats["avg_60m"]:
                                        fig_hist.add_vline(
                                            x=stats["avg_60m"],
                                            line_dash="dot",
                                            line_color="blue",
                                            annotation_text=f"Avg ({stats['avg_60m']:.1f})",
                                        )
                                    st.plotly_chart(fig_hist, use_container_width=True)

                                with chart_col2:
                                    # Timeline of arrivals
                                    fig_timeline = px.scatter(
                                        comparison_df,
                                        x="minutes_before",
                                        y="wait_time_min",
                                        title="Wait Times by Arrival Time (minutes before target)",
                                        labels={
                                            "minutes_before": "Minutes Before Target Dasher",
                                            "wait_time_min": "Wait Time (min)",
                                        },
                                    )
                                    # Add the target dasher as a distinct point
                                    fig_timeline.add_trace(go.Scatter(
                                        x=[0],
                                        y=[delivery["wait_time_min"]],
                                        mode="markers",
                                        marker=dict(color="red", size=15, symbol="star"),
                                        name="Target Dasher",
                                    ))
                                    st.plotly_chart(fig_timeline, use_container_width=True)

                                # Individual comparison table
                                st.subheader("Individual Comparisons")
                                st.dataframe(
                                    comparison_df,
                                    use_container_width=True,
                                    height=300,
                                    column_config={
                                        "delivery_id": st.column_config.NumberColumn("Delivery ID", format="%d"),
                                        "dasher_id": st.column_config.NumberColumn("Dasher ID", format="%d"),
                                        "arrival_time": st.column_config.DatetimeColumn("Arrival Time"),
                                        "wait_time_min": st.column_config.NumberColumn("Wait (min)", format="%.1f"),
                                        "minutes_before": st.column_config.NumberColumn("Min Before", format="%d"),
                                    },
                                )

                            st.divider()

                            # Store historical stats
                            st.subheader("Store Historical Statistics")
                            st.markdown(f"Based on last {lookback_days} days of deliveries at this store.")

                            store_stats = get_store_historical_stats(
                                store_id=delivery["store_id"],
                                as_of_date=pd.to_datetime(arrival_time).date(),
                                lookback_days=lookback_days,
                            )

                            if store_stats:
                                stat_col1, stat_col2, stat_col3, stat_col4, stat_col5 = st.columns(5)
                                with stat_col1:
                                    st.metric("Total Deliveries", int(store_stats["total_deliveries"]))
                                with stat_col2:
                                    st.metric("P50 (Median)", f"{store_stats['p50_wait_min']:.1f} min")
                                with stat_col3:
                                    st.metric("P75", f"{store_stats['p75_wait_min']:.1f} min")
                                with stat_col4:
                                    st.metric("P90", f"{store_stats['p90_wait_min']:.1f} min")
                                with stat_col5:
                                    st.metric("P99", f"{store_stats['p99_wait_min']:.1f} min")

                                # Compare to store median
                                if store_stats["p50_wait_min"] and delivery["wait_time_min"]:
                                    store_ratio = delivery["wait_time_min"] / store_stats["p50_wait_min"]
                                    if store_ratio > 2:
                                        st.warning(
                                            f"This delivery's wait ({delivery['wait_time_min']:.1f} min) is "
                                            f"**{store_ratio:.1f}x the store median** ({store_stats['p50_wait_min']:.1f} min)."
                                        )
                                    else:
                                        st.info(
                                            f"This delivery's wait ({delivery['wait_time_min']:.1f} min) is "
                                            f"**{store_ratio:.1f}x the store median** ({store_stats['p50_wait_min']:.1f} min)."
                                        )
                            else:
                                st.info("No historical data available for this store.")

                    else:
                        if not arrival_time:
                            st.warning("No store arrival time recorded for this delivery - cannot perform comparison.")
                        elif not delivery["wait_time_min"]:
                            st.warning("No wait time recorded for this delivery.")
                        else:
                            st.warning("Missing store information for this delivery.")

            except Exception as e:
                st.error(f"Error fetching data: {str(e)}")
                st.exception(e)
else:
    st.info("Enter a Delivery ID in the sidebar and click Analyze to begin.")
    st.markdown("""
    ### How This Tool Works

    1. **Enter a delivery ID** - The tool fetches delivery details including store, wait time, and lateness
    2. **Compares against peers** - Finds other dashers who arrived at the same store within 60 minutes before
    3. **Shows lookback windows** - Compares average wait times for 10, 30, and 60 minute windows
    4. **Interprets the gap** - Flags if the dasher's wait time is significantly above peers

    ### Interpretation Guide

    | Gap Ratio | Interpretation |
    |-----------|----------------|
    | 3x+ | Store slowness claim not supported |
    | 2-3x | Elevated wait time |
    | 1.5-2x | Moderately above average |
    | <1.5x | Within normal range |
    """)
