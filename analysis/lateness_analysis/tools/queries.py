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
    # Snow CLI v3 config location
    config_path = Path.home() / "Library" / "Application Support" / "snowflake" / "config.toml"

    if not config_path.exists():
        # Fallback to Linux/other OS location
        config_path = Path.home() / ".config" / "snowflake" / "config.toml"

    if not config_path.exists():
        raise FileNotFoundError(
            f"Snowflake config not found. Expected at:\n"
            f"  - ~/Library/Application Support/snowflake/config.toml (macOS)\n"
            f"  - ~/.config/snowflake/config.toml (Linux)"
        )

    with open(config_path, "rb") as f:
        config = tomllib.load(f)

    # Find the default connection or first available
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


def get_dasher_deliveries(dasher_id: int, lookback_days: int = 28, as_of_date: date = None) -> pd.DataFrame:
    """Fetch all deliveries for a dasher within the lookback period."""
    if as_of_date is None:
        as_of_date = date.today()
    date_str = as_of_date.strftime("%Y-%m-%d")

    query = f"""
    SELECT
        delivery_id,
        assignment_created_at::date AS delivery_date,
        ROUND(EST_ACT_PICKUP_ERR_MINUTES, 2) AS pickup_late_min,
        ROUND(EST_ACT_DROPOFF_ERR_MINUTES, 2) AS dropoff_late_min,
        ROUND(EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES, 2) AS total_late_min,
        ROUND(DELIVERY_DEVIATION_SCORE, 2) AS deviation_score
    FROM edw.opex.fact_dx_fraud_pc_rolling_scores
    WHERE dasher_id = {dasher_id}
      AND timebased_pay_model NOT IN ('order mode')
      AND assignment_created_at >= dateadd(dd, -{lookback_days}, '{date_str}'::date)
      AND assignment_created_at <= '{date_str}'::date
    ORDER BY assignment_created_at DESC
    """

    conn = get_snowflake_connection()
    try:
        df = pd.read_sql(query, conn)
        df.columns = df.columns.str.lower()
        return df
    finally:
        conn.close()


def get_dasher_summary(dasher_id: int, lookback_days: int = 28, threshold: int = 20, as_of_date: date = None) -> dict:
    """Get aggregate statistics for a dasher."""
    if as_of_date is None:
        as_of_date = date.today()
    date_str = as_of_date.strftime("%Y-%m-%d")

    query = f"""
    SELECT
        COUNT(*) AS total_deliveries,
        ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EST_ACT_PICKUP_ERR_MINUTES), 2) AS median_pickup_min,
        ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EST_ACT_DROPOFF_ERR_MINUTES), 2) AS median_dropoff_min,
        ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES), 2) AS median_total_late_min,
        SUM(CASE WHEN (EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES) > {threshold} THEN 1 ELSE 0 END) AS deliveries_over_threshold,
        SUM(CASE WHEN (EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES) > 30 THEN 1 ELSE 0 END) AS deliveries_over_30,
        SUM(CASE WHEN (EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES) > 15 THEN 1 ELSE 0 END) AS deliveries_over_15,
        SUM(CASE WHEN (EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES) > 10 THEN 1 ELSE 0 END) AS deliveries_over_10
    FROM edw.opex.fact_dx_fraud_pc_rolling_scores
    WHERE dasher_id = {dasher_id}
      AND timebased_pay_model NOT IN ('order mode')
      AND assignment_created_at >= dateadd(dd, -{lookback_days}, '{date_str}'::date)
      AND assignment_created_at <= '{date_str}'::date
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


def classify_tier(summary: dict) -> str:
    """Classify dasher into risk tier based on lateness patterns."""
    if summary is None:
        return "No Data"

    total = summary["total_deliveries"]
    if total == 0:
        return "No Data"

    pct_over_30 = summary["deliveries_over_30"] / total
    pct_over_15 = summary["deliveries_over_15"] / total
    pct_over_10 = summary["deliveries_over_10"] / total

    if pct_over_30 > 0.5:
        return "Tier 1 (Egregious)"
    elif pct_over_15 > 0.5:
        return "Tier 2 (Moderate)"
    elif pct_over_10 > 0.5:
        return "Tier 3 (Mild)"
    else:
        return "Normal"


def detect_pattern(summary: dict) -> str:
    """Detect lateness pattern type."""
    if summary is None:
        return "Unknown"

    median_pickup = summary.get("median_pickup_min", 0) or 0
    median_dropoff = summary.get("median_dropoff_min", 0) or 0

    if median_pickup < 5 and median_dropoff > 30:
        return "Dropoff-Heavy"
    elif median_pickup > 20 and median_dropoff < 10:
        return "Pickup-Heavy"
    else:
        return "Mixed"
