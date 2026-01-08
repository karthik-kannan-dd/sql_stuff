# Lateness Distribution: Histogram Analysis

> **Analysis Date:** January 7, 2026
> **Data Source:** `edw.opex.fact_dx_fraud_pc_rolling_scores`
> **Scope:** Dashers with 20+ TBPM deliveries in last 28 days
> **Lateness Metric:** Total Lateness = Pickup Lateness + Dropoff Lateness
> **Late Threshold:** >10 minutes total late (Tier 3+ threshold)

---

## Summary

Distribution of TBPM dashers by what percentage of their deliveries are late (>10 min total lateness).

**Key Finding:** The vast majority of dashers (64.7%) have ≤5% of their deliveries >10 min late. Only 0.16% of dashers (419 dashers) have >50% of deliveries late - these are flagged as Tier 3 or higher risk.

---

## Histogram: Distribution of Dashers by % Late Deliveries

| % of Deliveries >10min Late | Dasher Count | Deliveries | % of Dashers | Visual |
|-----------------------------|--------------|------------|--------------|--------|
| **0%** | 37,259 | 1,948,672 | 13.81% | `███████` |
| **1-5%** | 137,359 | 23,360,673 | 50.90% | `█████████████████████████` |
| **6-10%** | 57,922 | 6,219,738 | 21.46% | `███████████` |
| **11-15%** | 19,952 | 1,594,793 | 7.39% | `████` |
| **16-20%** | 8,638 | 604,096 | 3.20% | `██` |
| **21-30%** | 5,971 | 368,819 | 2.21% | `█` |
| **31-40%** | 1,690 | 95,536 | 0.63% | `▌` |
| **41-50%** | 641 | 33,704 | 0.24% | `▏` |
| **51-60%** | 229 | 14,032 | 0.08% | |
| **61-70%** | 112 | 5,526 | 0.04% | |
| **71-80%** | 42 | 1,735 | 0.02% | |
| **81-90%** | 26 | 883 | 0.01% | |
| **91-100%** | 10 | 526 | 0.00% | |

**Total Dashers Analyzed:** 269,851
**Total Deliveries Analyzed:** 34,248,733

---

## Key Insights

### The Good News
- **64.7% of dashers** have ≤5% of deliveries >10 min late
- **13.8% of dashers** have 0% late deliveries (>10 min)
- Most dashers are consistently on-time

### The Long Tail (Risk Population)

| Bucket | Dashers | Deliveries | % of All Dashers |
|--------|---------|------------|------------------|
| >50% late (Tier 3+) | 419 | 22,702 | 0.16% |
| >30% late | 2,750 | 151,942 | 1.02% |
| >20% late | 8,721 | 520,761 | 3.23% |

### Tier Alignment

| Tier | Criteria | Dashers |
|------|----------|---------|
| **Tier 1: Egregious** | >50% deliveries >30 min total late | 14 dashers |
| **Tier 2: Moderate** | >50% deliveries >15 min (excl Tier 1) | 77 dashers |
| **Tier 3: Mild** | >50% deliveries >10 min (excl Tier 1-2) | 329 dashers |
| **Total at-risk** | >50% deliveries >10 min total late | **420 dashers** |

### Cumulative Distribution

| Threshold | Dashers Above | Deliveries | % of All Dashers |
|-----------|---------------|------------|------------------|
| >5% late (>10 min) | 95,233 | 9,335,423 | 35.29% |
| >10% late | 37,311 | 3,115,685 | 13.83% |
| >20% late | 8,721 | 520,761 | 3.23% |
| >30% late | 2,750 | 151,942 | 1.02% |
| >50% late (Tier 3+) | 419 | 22,702 | 0.16% |

---

## SQL Query

```sql
WITH dasher_stats AS (
    SELECT
        dasher_id,
        COUNT(*) AS total_deliveries,
        SUM(CASE WHEN (EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES) > 30 THEN 1 ELSE 0 END) AS count_over_30min,
        SUM(CASE WHEN (EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES) > 15 THEN 1 ELSE 0 END) AS count_over_15min,
        SUM(CASE WHEN (EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES) > 10 THEN 1 ELSE 0 END) AS count_over_10min,
        100.0 * SUM(CASE WHEN (EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES) > 10 THEN 1 ELSE 0 END) / COUNT(*) AS pct_over_10min
    FROM edw.opex.fact_dx_fraud_pc_rolling_scores
    WHERE timebased_pay_model NOT IN ('order mode')
      AND assignment_created_at >= dateadd(dd,-28,current_date())
      AND DELIVERY_DEVIATION_SCORE IS NOT NULL
    GROUP BY dasher_id
    HAVING COUNT(*) >= 20
)
SELECT
    CASE
        WHEN pct_over_10min = 0 THEN '0%'
        WHEN pct_over_10min > 0 AND pct_over_10min <= 5 THEN '1-5%'
        WHEN pct_over_10min > 5 AND pct_over_10min <= 10 THEN '6-10%'
        WHEN pct_over_10min > 10 AND pct_over_10min <= 15 THEN '11-15%'
        WHEN pct_over_10min > 15 AND pct_over_10min <= 20 THEN '16-20%'
        WHEN pct_over_10min > 20 AND pct_over_10min <= 30 THEN '21-30%'
        WHEN pct_over_10min > 30 AND pct_over_10min <= 40 THEN '31-40%'
        WHEN pct_over_10min > 40 AND pct_over_10min <= 50 THEN '41-50%'
        WHEN pct_over_10min > 50 AND pct_over_10min <= 60 THEN '51-60%'
        WHEN pct_over_10min > 60 AND pct_over_10min <= 70 THEN '61-70%'
        WHEN pct_over_10min > 70 AND pct_over_10min <= 80 THEN '71-80%'
        WHEN pct_over_10min > 80 AND pct_over_10min <= 90 THEN '81-90%'
        ELSE '91-100%'
    END AS pct_late_bucket,
    COUNT(*) AS dasher_count,
    SUM(total_deliveries) AS total_deliveries,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) AS pct_of_all_dashers
FROM dasher_stats
GROUP BY 1
ORDER BY pct_late_bucket;
```

---

*Analysis conducted January 7, 2026*
