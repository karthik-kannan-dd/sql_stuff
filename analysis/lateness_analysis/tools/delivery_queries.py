import sys
from datetime import date
from pathlib import Path

import pandas as pd
import snowflake.connector

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


def get_snowflake_connection():
    """Read credentials from snow CLI config.toml and return a Snowflake connection."""
    config_path = Path.home() / "Library" / "Application Support" / "snowflake" / "config.toml"

    if not config_path.exists():
        config_path = Path.home() / ".config" / "snowflake" / "config.toml"

    if not config_path.exists():
        raise FileNotFoundError(
            f"Snowflake config not found. Expected at:\n"
            f"  - ~/Library/Application Support/snowflake/config.toml (macOS)\n"
            f"  - ~/.config/snowflake/config.toml (Linux)"
        )

    with open(config_path, "rb") as f:
        config = tomllib.load(f)

    connections = config.get("connections", {})
    default_conn_name = config.get("default_connection_name", None)

    if default_conn_name and default_conn_name in connections:
        conn_config = connections[default_conn_name]
    elif connections:
        conn_config = list(connections.values())[0]
    else:
        raise ValueError("No connections found in config.toml")

    conn_params = {
        "account": conn_config.get("account"),
        "user": conn_config.get("user"),
        "password": conn_config.get("password"),
        "warehouse": conn_config.get("warehouse"),
        "database": conn_config.get("database"),
        "schema": conn_config.get("schema"),
    }

    conn_params = {k: v for k, v in conn_params.items() if v is not None}

    return snowflake.connector.connect(**conn_params)


def get_delivery_details(delivery_id: int, start_date: date, end_date: date) -> dict:
    """Fetch delivery details including store info and wait times."""
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")

    query = f"""
    SELECT
        pc.delivery_id,
        pc.dasher_id,
        dd.store_id,
        dd.store_name,
        pc.assignment_created_at,
        fa.DASHER_CONFIRMED_STORE_ARRIVAL_TIME AS store_arrival_time,
        ROUND(fa.MX_ARRIVAL_TO_PICKUP_SECOND / 60.0, 2) AS wait_time_min,
        ROUND(pc.EST_ACT_PICKUP_ERR_MINUTES, 2) AS pickup_late_min,
        ROUND(pc.EST_ACT_DROPOFF_ERR_MINUTES, 2) AS dropoff_late_min,
        ROUND(pc.EST_ACT_PICKUP_ERR_MINUTES + pc.EST_ACT_DROPOFF_ERR_MINUTES, 2) AS total_late_min,
        ROUND(pc.DELIVERY_DEVIATION_SCORE, 2) AS deviation_score,
        pc.timebased_pay_model
    FROM edw.opex.fact_dx_fraud_pc_rolling_scores pc
    JOIN proddb.public.dimension_deliveries dd
        ON pc.delivery_id = dd.delivery_id
        AND dd.active_date >= '{start_str}'::date
        AND dd.active_date <= '{end_str}'::date
    JOIN edw.opex.fact_dx_fraud_assignment fa
        ON pc.delivery_id = fa.delivery_id
        AND fa.is_last_assignment = TRUE
    WHERE pc.delivery_id = {delivery_id}
      AND pc.assignment_created_at >= '{start_str}'::date
      AND pc.assignment_created_at <= '{end_str}'::date
    """

    conn = get_snowflake_connection()
    try:
        df = pd.read_sql(query, conn)
        df.columns = df.columns.str.lower()
        if df.empty:
            return None
        return df.iloc[0].to_dict()
    finally:
        conn.close()


def get_store_wait_comparison(
    store_id: int,
    store_arrival_time: str,
    dasher_id: int,
    lookback_days: int = 28,
) -> pd.DataFrame:
    """
    Compare wait times at a store with other dashers who arrived within lookback windows.

    Returns a dataframe with other dashers' wait times, bucketed by how many minutes
    before the target arrival time they arrived.
    """
    query = f"""
    WITH other_dashers AS (
        SELECT
            fa.delivery_id,
            fa.dasher_id,
            fa.DASHER_CONFIRMED_STORE_ARRIVAL_TIME AS arrival_time,
            ROUND(fa.MX_ARRIVAL_TO_PICKUP_SECOND / 60.0, 2) AS wait_time_min,
            DATEDIFF('minute', fa.DASHER_CONFIRMED_STORE_ARRIVAL_TIME, '{store_arrival_time}'::timestamp) AS minutes_before
        FROM proddb.public.dimension_deliveries dd
        JOIN edw.opex.fact_dx_fraud_assignment fa
            ON fa.delivery_id = dd.delivery_id
            AND fa.is_last_assignment = TRUE
        WHERE dd.store_id = {store_id}
          AND dd.active_date >= DATEADD('day', -{lookback_days}, '{store_arrival_time}'::date)
          AND dd.active_date <= '{store_arrival_time}'::date
          AND fa.dasher_id != {dasher_id}
          AND fa.DASHER_CONFIRMED_STORE_ARRIVAL_TIME IS NOT NULL
          AND fa.MX_ARRIVAL_TO_PICKUP_SECOND IS NOT NULL
          AND fa.DASHER_CONFIRMED_STORE_ARRIVAL_TIME >= DATEADD('minute', -60, '{store_arrival_time}'::timestamp)
          AND fa.DASHER_CONFIRMED_STORE_ARRIVAL_TIME <= '{store_arrival_time}'::timestamp
    )
    SELECT
        delivery_id,
        dasher_id,
        arrival_time,
        wait_time_min,
        minutes_before
    FROM other_dashers
    ORDER BY minutes_before ASC
    """

    conn = get_snowflake_connection()
    try:
        df = pd.read_sql(query, conn)
        df.columns = df.columns.str.lower()
        return df
    finally:
        conn.close()


def get_store_historical_stats(
    store_id: int,
    as_of_date: date,
    lookback_days: int = 28,
) -> dict:
    """Get historical wait time statistics for a store."""
    date_str = as_of_date.strftime("%Y-%m-%d")

    query = f"""
    SELECT
        COUNT(*) AS total_deliveries,
        ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY fa.MX_ARRIVAL_TO_PICKUP_SECOND / 60.0), 2) AS p50_wait_min,
        ROUND(PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY fa.MX_ARRIVAL_TO_PICKUP_SECOND / 60.0), 2) AS p75_wait_min,
        ROUND(PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY fa.MX_ARRIVAL_TO_PICKUP_SECOND / 60.0), 2) AS p90_wait_min,
        ROUND(PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY fa.MX_ARRIVAL_TO_PICKUP_SECOND / 60.0), 2) AS p99_wait_min
    FROM proddb.public.dimension_deliveries dd
    JOIN edw.opex.fact_dx_fraud_assignment fa
        ON fa.delivery_id = dd.delivery_id
        AND fa.is_last_assignment = TRUE
    WHERE dd.store_id = {store_id}
      AND dd.active_date >= DATEADD('day', -{lookback_days}, '{date_str}'::date)
      AND dd.active_date <= '{date_str}'::date
      AND fa.MX_ARRIVAL_TO_PICKUP_SECOND IS NOT NULL
    """

    conn = get_snowflake_connection()
    try:
        df = pd.read_sql(query, conn)
        df.columns = df.columns.str.lower()
        if df.empty or df.iloc[0]["total_deliveries"] == 0:
            return None
        return df.iloc[0].to_dict()
    finally:
        conn.close()


def compute_comparison_stats(comparison_df: pd.DataFrame, target_wait: float) -> dict:
    """Compute comparison statistics from the other dashers dataframe."""
    if comparison_df.empty:
        return {
            "n_10m": 0, "avg_10m": None,
            "n_30m": 0, "avg_30m": None,
            "n_60m": 0, "avg_60m": None,
            "target_wait": target_wait,
        }

    df = comparison_df

    n_10m = len(df[df["minutes_before"] <= 10])
    n_30m = len(df[df["minutes_before"] <= 30])
    n_60m = len(df)

    avg_10m = df[df["minutes_before"] <= 10]["wait_time_min"].mean() if n_10m > 0 else None
    avg_30m = df[df["minutes_before"] <= 30]["wait_time_min"].mean() if n_30m > 0 else None
    avg_60m = df["wait_time_min"].mean() if n_60m > 0 else None

    return {
        "n_10m": n_10m,
        "avg_10m": round(avg_10m, 1) if avg_10m is not None else None,
        "n_30m": n_30m,
        "avg_30m": round(avg_30m, 1) if avg_30m is not None else None,
        "n_60m": n_60m,
        "avg_60m": round(avg_60m, 1) if avg_60m is not None else None,
        "target_wait": target_wait,
    }
