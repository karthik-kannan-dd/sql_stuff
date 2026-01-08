from datetime import date, timedelta

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from queries import (
    get_dasher_deliveries,
    get_dasher_summary,
    classify_tier,
    detect_pattern,
)

st.set_page_config(
    page_title="Dasher Lateness Lookup",
    page_icon="clock",
    layout="wide",
)

st.title("Dasher Lateness Lookup Tool")
st.markdown("Look up late deliveries for a dasher with configurable lateness threshold.")

# Sidebar inputs
st.sidebar.header("Parameters")

dasher_id = st.sidebar.number_input(
    "Dasher ID",
    min_value=1,
    value=None,
    placeholder="Enter Dasher ID",
    help="Enter the dasher ID to look up",
)

lateness_threshold = st.sidebar.slider(
    "Lateness Threshold (minutes)",
    min_value=0,
    max_value=120,
    value=20,
    help="Flag deliveries with total lateness above this threshold",
)

lookback_days = st.sidebar.slider(
    "Lookback Period (days)",
    min_value=7,
    max_value=90,
    value=28,
    help="Number of days to look back for deliveries",
)

as_of_date = st.sidebar.date_input(
    "As of Date",
    value=date.today(),
    max_value=date.today(),
    help="Reference date to look back from (defaults to today)",
)

if st.sidebar.button("Search", type="primary") or dasher_id:
    if not dasher_id:
        st.warning("Please enter a Dasher ID")
    else:
        with st.spinner("Fetching data from Snowflake..."):
            try:
                summary = get_dasher_summary(dasher_id, lookback_days, lateness_threshold, as_of_date)
                deliveries = get_dasher_deliveries(dasher_id, lookback_days, as_of_date)

                if summary is None or deliveries.empty:
                    st.error(f"No deliveries found for Dasher {dasher_id} in the last {lookback_days} days")
                else:
                    tier = classify_tier(summary)
                    pattern = detect_pattern(summary)

                    # Summary metrics
                    st.header("Summary")
                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.metric("Total Deliveries", int(summary["total_deliveries"]))
                    with col2:
                        st.metric("Median Total Lateness", f"{summary['median_total_late_min']:.1f} min")
                    with col3:
                        pct_over = (summary["deliveries_over_threshold"] / summary["total_deliveries"]) * 100
                        st.metric(
                            f"Over {lateness_threshold} min",
                            f"{int(summary['deliveries_over_threshold'])} ({pct_over:.0f}%)",
                        )
                    with col4:
                        st.metric("Risk Tier", tier)

                    # Pattern and breakdown
                    col5, col6, col7 = st.columns(3)
                    with col5:
                        st.metric("Pattern Type", pattern)
                    with col6:
                        st.metric("Median Pickup Lateness", f"{summary['median_pickup_min']:.1f} min")
                    with col7:
                        st.metric("Median Dropoff Lateness", f"{summary['median_dropoff_min']:.1f} min")

                    # Tier alert
                    if tier == "Tier 1 (Egregious)":
                        st.error(f"ALERT: Dasher {dasher_id} is classified as **Tier 1 (Egregious)** - >50% of deliveries are 30+ minutes late")
                    elif tier == "Tier 2 (Moderate)":
                        st.warning(f"WARNING: Dasher {dasher_id} is classified as **Tier 2 (Moderate)** - >50% of deliveries are 15+ minutes late")
                    elif tier == "Tier 3 (Mild)":
                        st.info(f"NOTE: Dasher {dasher_id} is classified as **Tier 3 (Mild)** - >50% of deliveries are 10+ minutes late")

                    st.divider()

                    # Charts
                    st.header("Charts")
                    chart_col1, chart_col2 = st.columns(2)

                    with chart_col1:
                        # Histogram of total lateness
                        fig_hist = px.histogram(
                            deliveries,
                            x="total_late_min",
                            nbins=30,
                            title="Distribution of Total Lateness",
                            labels={"total_late_min": "Total Lateness (min)", "count": "Count"},
                        )
                        fig_hist.add_vline(
                            x=lateness_threshold,
                            line_dash="dash",
                            line_color="red",
                            annotation_text=f"Threshold ({lateness_threshold} min)",
                        )
                        st.plotly_chart(fig_hist, use_container_width=True)

                    with chart_col2:
                        # Pickup vs Dropoff scatter
                        fig_scatter = px.scatter(
                            deliveries,
                            x="pickup_late_min",
                            y="dropoff_late_min",
                            color="total_late_min",
                            title="Pickup vs Dropoff Lateness",
                            labels={
                                "pickup_late_min": "Pickup Lateness (min)",
                                "dropoff_late_min": "Dropoff Lateness (min)",
                                "total_late_min": "Total (min)",
                            },
                            color_continuous_scale="RdYlGn_r",
                        )
                        st.plotly_chart(fig_scatter, use_container_width=True)

                    # Time series
                    daily_avg = deliveries.groupby("delivery_date").agg({
                        "total_late_min": "mean",
                        "pickup_late_min": "mean",
                        "dropoff_late_min": "mean",
                        "delivery_id": "count",
                    }).reset_index()
                    daily_avg.columns = ["date", "avg_total_late", "avg_pickup_late", "avg_dropoff_late", "delivery_count"]

                    fig_time = go.Figure()
                    fig_time.add_trace(go.Scatter(
                        x=daily_avg["date"],
                        y=daily_avg["avg_total_late"],
                        mode="lines+markers",
                        name="Total Lateness",
                        line=dict(color="blue"),
                    ))
                    fig_time.add_trace(go.Scatter(
                        x=daily_avg["date"],
                        y=daily_avg["avg_pickup_late"],
                        mode="lines+markers",
                        name="Pickup Lateness",
                        line=dict(color="orange"),
                    ))
                    fig_time.add_trace(go.Scatter(
                        x=daily_avg["date"],
                        y=daily_avg["avg_dropoff_late"],
                        mode="lines+markers",
                        name="Dropoff Lateness",
                        line=dict(color="green"),
                    ))
                    fig_time.add_hline(
                        y=lateness_threshold,
                        line_dash="dash",
                        line_color="red",
                        annotation_text=f"Threshold",
                    )
                    fig_time.update_layout(
                        title="Lateness Over Time (Daily Average)",
                        xaxis_title="Date",
                        yaxis_title="Lateness (min)",
                    )
                    st.plotly_chart(fig_time, use_container_width=True)

                    st.divider()

                    # Delivery table
                    st.header("Delivery Details")

                    # Add highlighting for over-threshold deliveries
                    def highlight_late(row):
                        if row["total_late_min"] > lateness_threshold:
                            return ["background-color: #ffcccc"] * len(row)
                        return [""] * len(row)

                    styled_df = deliveries.style.apply(highlight_late, axis=1)
                    st.dataframe(
                        styled_df,
                        use_container_width=True,
                        height=400,
                        column_config={
                            "delivery_id": st.column_config.NumberColumn("Delivery ID", format="%d"),
                            "delivery_date": st.column_config.DateColumn("Date"),
                            "pickup_late_min": st.column_config.NumberColumn("Pickup (min)", format="%.1f"),
                            "dropoff_late_min": st.column_config.NumberColumn("Dropoff (min)", format="%.1f"),
                            "total_late_min": st.column_config.NumberColumn("Total (min)", format="%.1f"),
                            "deviation_score": st.column_config.NumberColumn("Deviation Score", format="%.2f"),
                        },
                    )

                    # Download button
                    csv = deliveries.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"dasher_{dasher_id}_lateness.csv",
                        mime="text/csv",
                    )

            except Exception as e:
                st.error(f"Error fetching data: {str(e)}")
                st.exception(e)
else:
    st.info("Enter a Dasher ID in the sidebar and click Search to begin.")
