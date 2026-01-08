# Fact DX Fraud PC Rolling Scores - Table Schema

> **Table:** `edw.opex.fact_dx_fraud_pc_rolling_scores`

This table contains lateness/deviation scores for deliveries, including both per-delivery metrics and rolling aggregates.

---

## Key Columns for Lateness Analysis

### Per-Delivery Metrics

| Column | Type | Description |
|--------|------|-------------|
| `DELIVERY_ID` | NUMBER | Unique identifier for the delivery |
| `DASHER_ID` | NUMBER | Unique identifier of the assigned Dasher |
| `ASSIGNMENT_CREATED_AT` | TIMESTAMP | When the delivery assignment was created |
| `EST_ACT_PICKUP_ERR_MINUTES` | NUMBER | Difference between estimated and actual pickup time (minutes) |
| `EST_ACT_DROPOFF_ERR_MINUTES` | NUMBER | Difference between estimated and actual dropoff time (minutes) |
| `PICKUP_DEVIATION_SCORE` | FLOAT | Score measuring deviation from expected pickup behavior |
| `DROPOFF_DEVIATION_SCORE` | FLOAT | Score measuring deviation from expected dropoff behavior |
| `DELIVERY_DEVIATION_SCORE` | FLOAT | **Overall score summarizing delivery timing deviations** |

### Rolling Aggregate Metrics

Rolling scores are computed over the last N deliveries (L = Last):

| Window | Sum Column | Avg Column | Count Column |
|--------|------------|------------|--------------|
| Last 10 | `DELIVERY_DEVIATION_SCORE_SUM_L10` | `DELIVERY_DEVIATION_SCORE_AVG_L10` | `DELIVERY_DEVIATION_SCORE_COUNT_L10` |
| Last 25 | `DELIVERY_DEVIATION_SCORE_SUM_L25` | `DELIVERY_DEVIATION_SCORE_AVG_L25` | `DELIVERY_DEVIATION_SCORE_COUNT_L25` |
| Last 50 | `DELIVERY_DEVIATION_SCORE_SUM_L50` | `DELIVERY_DEVIATION_SCORE_AVG_L50` | `DELIVERY_DEVIATION_SCORE_COUNT_L50` |
| Last 100 | `DELIVERY_DEVIATION_SCORE_SUM_L100` | `DELIVERY_DEVIATION_SCORE_AVG_L100` | `DELIVERY_DEVIATION_SCORE_COUNT_L100` |

### TBPM-Specific Rolling Metrics

Same structure exists for Time-Based Pay Model (TBPM) deliveries:
- `DELIVERY_DEVIATION_SCORE_AVG_L50_TBPM`
- `DELIVERY_DEVIATION_SCORE_AVG_L100_TBPM`
- etc.

### Predictive Columns

| Column | Description |
|--------|-------------|
| `PREDICTED_MINUTES_LATE_PICKUP` | Forecasted lateness for pickup |
| `PREDICTED_MINUTES_LATE_DROPOFF` | Forecasted lateness for dropoff |
| `PREDICTED_MINUTES_LATE_PICKUP_OBS_CI_LOWER/UPPER` | Confidence intervals |
| `PREDICTED_MINUTES_LATE_DROPOFF_OBS_CI_LOWER/UPPER` | Confidence intervals |

---

## Score Interpretation

- **`DELIVERY_DEVIATION_SCORE`**: Higher scores indicate worse performance (more deviation from expected timing)
- **Positive `EST_ACT_*_ERR_MINUTES`**: Dasher was LATE (actual > estimated)
- **Negative `EST_ACT_*_ERR_MINUTES`**: Dasher was EARLY (actual < estimated)

---

## Analysis Strategy

To identify dashers with worst lateness patterns:

1. **Find highest `DELIVERY_DEVIATION_SCORE_AVG_L50`** - Consistent lateness over 50 deliveries
2. **Compare `DELIVERY_DEVIATION_SCORE_AVG_L50` vs max single `DELIVERY_DEVIATION_SCORE`** - Distinguish consistent vs outlier behavior
3. **Check if high avg is driven by single outliers** - Compare L10, L25, L50, L100 averages

---

*Generated: December 30, 2025*
