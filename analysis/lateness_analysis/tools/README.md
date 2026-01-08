# Dasher Lateness Lookup Tool

A Streamlit web app to look up late deliveries for a given dasher ID.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure Snowflake credentials are configured in `~/.snowsql/config`

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| Dasher ID | The dasher to look up | Required |
| Lateness Threshold | Flag deliveries above this threshold (minutes) | 20 |
| Lookback Period | Number of days to look back | 28 |

## Output

### Summary Stats
- Total deliveries in period
- Median pickup/dropoff/total lateness
- Count & percentage of deliveries over threshold
- Risk tier classification (Tier 1/2/3)
- Pattern type (Dropoff-Heavy, Pickup-Heavy, Mixed)

### Charts
- Histogram of total lateness distribution
- Pickup vs Dropoff scatter plot
- Time series of daily average lateness

### Delivery Table
- All deliveries with lateness details
- Rows over threshold highlighted in red
- Downloadable as CSV

## Risk Tiers

| Tier | Criteria |
|------|----------|
| Tier 1 (Egregious) | >50% deliveries with total lateness >60 min |
| Tier 2 (Moderate) | >50% with total lateness >30 min |
| Tier 3 (Mild) | >50% with total lateness >20 min |

## Pattern Types

| Pattern | Criteria |
|---------|----------|
| Dropoff-Heavy | Median pickup < 5 min, median dropoff > 60 min |
| Pickup-Heavy | Median pickup > 30 min, median dropoff < 15 min |
| Mixed | Neither pattern |

## Data Source

Table: `edw.opex.fact_dx_fraud_pc_rolling_scores`

Total lateness = `EST_ACT_PICKUP_ERR_MINUTES` + `EST_ACT_DROPOFF_ERR_MINUTES`
