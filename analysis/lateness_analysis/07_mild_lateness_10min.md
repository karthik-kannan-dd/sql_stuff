# Tier 3: Mild Lateness Analysis

> **Analysis Date:** January 8, 2026
> **Data Source:** `edw.opex.fact_dx_fraud_pc_rolling_scores`
> **Data Period:** December 10, 2025 - January 7, 2026 (28 days)
> **Scope:** Dashers with mild lateness patterns (excluding Tier 1-2)
> **Lateness Metric:** Total Lateness = Pickup Lateness + Dropoff Lateness

---

## Summary

**339 dashers** have mild lateness patterns: >50% of deliveries over 10 min total late, but ≤50% over 15 min.

### Tier 3 Overview

| Metric | Value |
|--------|-------|
| Dasher Count | 339 |
| Avg Median Pickup Late | 7.81 min |
| Avg Median Dropoff Late | 2.61 min |
| Avg Median Total Late | 11.81 min |
| Avg % >10 min late | 58.6% |
| Avg % >15 min late | 33.1% |
| Avg % >30 min late | 7.5% |

---

## Pattern Distribution

| Pattern | Dasher Count | % of Tier | Avg Pickup | Avg Dropoff | Avg Total |
|---------|--------------|-----------|------------|-------------|-----------|
| **Pickup-Heavy** | 146 | 43% | 11.32 min | -0.29 min | 11.75 min |
| **Mixed** | 131 | 39% | 5.37 min | 5.43 min | 12.10 min |
| **Other** | 56 | 17% | 4.97 min | 2.71 min | 11.16 min |
| **Dropoff-Heavy** | 6 | 2% | 2.14 min | 10.41 min | 13.07 min |

**Key observation:** Unlike Tier 1 (dominated by dropoff delays) and Tier 2 (pickup-heavy), Tier 3 is more evenly split between pickup-heavy and mixed patterns.

---

## Top 20 Tier 3 Dashers by % >10 min Late

| Dasher ID | Deliveries | Med Pickup | Med Dropoff | Med Total | % >10min | % >15min | % >30min | Notes |
|-----------|------------|------------|-------------|-----------|----------|----------|----------|-------|
| 67095195 | 23 | 5.38 min | 9.23 min | 14.70 min | 82.6% | 47.8% | 13.0% | |
| 56236833 | 141 | 5.85 min | 7.92 min | 13.67 min | 80.9% | 29.8% | 0.0% | |
| 52936187 | 126 | 5.13 min | 7.52 min | 12.53 min | 80.2% | 13.5% | 0.0% | |
| 44663937 | 20 | 6.22 min | 6.68 min | 13.17 min | 80.0% | 30.0% | 0.0% | |
| 47173157 | 26 | 12.23 min | 1.85 min | 14.73 min | 76.9% | 42.3% | 3.8% | |
| 56757343 | 29 | 7.43 min | 6.17 min | 12.63 min | 75.9% | 34.5% | 10.3% | |
| 61507016 | 20 | 10.46 min | 2.84 min | 13.07 min | 75.0% | 40.0% | 0.0% | |
| 67559440 | 20 | 8.15 min | 4.38 min | 13.11 min | 75.0% | 40.0% | 0.0% | |
| 35223698 | 27 | 13.75 min | 0.18 min | 13.82 min | 74.1% | 40.7% | 0.0% | |
| 65965673 | 38 | 3.83 min | 10.49 min | 15.15 min | 73.7% | 50.0% | 21.1% | |
| 64510056 | 48 | 6.63 min | 6.37 min | 15.01 min | 72.9% | 50.0% | 25.0% | |
| 66093192 | 22 | 4.08 min | 11.06 min | 14.83 min | 72.7% | 45.5% | 13.6% | |
| 29037055 | 47 | 14.10 min | -0.18 min | 13.98 min | 72.3% | 44.7% | 8.5% | |
| 67521044 | 36 | 4.99 min | 8.30 min | 15.21 min | 72.2% | 50.0% | 11.1% | |
| 7445250 | 43 | 11.60 min | 1.73 min | 13.93 min | 72.1% | 44.2% | 0.0% | |
| 36425466 | 25 | 4.07 min | 6.85 min | 13.37 min | 72.0% | 36.0% | 0.0% | |
| 66134391 | 25 | 2.78 min | 11.10 min | 13.95 min | 72.0% | 40.0% | 4.0% | |
| 59543594 | 21 | 12.20 min | -0.85 min | 13.63 min | 71.4% | 28.6% | 0.0% | |
| 59965008 | 45 | 5.97 min | 8.40 min | 14.50 min | 71.1% | 46.7% | 17.8% | |
| 65990751 | 24 | 6.70 min | 5.19 min | 13.41 min | 70.8% | 45.8% | 8.3% | |

---

## Key Differences from Tier 1-2

| Aspect | Tier 1 (Egregious) | Tier 2 (Moderate) | Tier 3 (Mild) |
|--------|-------------------|-------------------|---------------|
| Dasher count | 14 | 77 | 339 |
| % >30 min late | 56-94% | 3-48% | 0-25% |
| Median total late | 33-100 min | 17-28 min | 11-15 min |
| Primary pattern | Dropoff-heavy | Pickup-heavy | Split (pickup/mixed) |
| Severity | Extreme delays | Significant delays | Consistent mild delays |

---

## SQL Queries

### Find Tier 3 Dashers (>50% over 10 min, ≤50% over 15 min total late)

```sql
WITH dasher_medians AS (
    SELECT
        dasher_id,
        COUNT(*) AS total_deliveries,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EST_ACT_PICKUP_ERR_MINUTES) AS median_pickup_min,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EST_ACT_DROPOFF_ERR_MINUTES) AS median_dropoff_min,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES) AS median_total_late_min,
        SUM(CASE WHEN (EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES) > 30 THEN 1 ELSE 0 END) AS count_over_30min_total,
        SUM(CASE WHEN (EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES) > 15 THEN 1 ELSE 0 END) AS count_over_15min_total,
        SUM(CASE WHEN (EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES) > 10 THEN 1 ELSE 0 END) AS count_over_10min_total
    FROM edw.opex.fact_dx_fraud_pc_rolling_scores
    WHERE timebased_pay_model NOT IN ('order mode')
      AND assignment_created_at >= '2025-12-10'::date
      AND assignment_created_at <= '2026-01-07'::date
      AND DELIVERY_DEVIATION_SCORE IS NOT NULL
    GROUP BY dasher_id
    HAVING COUNT(*) >= 20
)
SELECT
    dasher_id,
    total_deliveries,
    ROUND(median_pickup_min, 2) AS median_pickup_min,
    ROUND(median_dropoff_min, 2) AS median_dropoff_min,
    ROUND(median_total_late_min, 2) AS median_total_late_min,
    ROUND(100.0 * count_over_10min_total / total_deliveries, 1) AS pct_over_10min,
    ROUND(100.0 * count_over_15min_total / total_deliveries, 1) AS pct_over_15min,
    ROUND(100.0 * count_over_30min_total / total_deliveries, 1) AS pct_over_30min
FROM dasher_medians
WHERE (100.0 * count_over_10min_total / total_deliveries) > 50  -- >50% over 10 min
  AND (100.0 * count_over_15min_total / total_deliveries) <= 50 -- Exclude Tier 1-2
ORDER BY pct_over_10min DESC, total_deliveries DESC;
```

### Pattern Distribution Query

```sql
WITH dasher_medians AS (
    SELECT
        dasher_id,
        COUNT(*) AS total_deliveries,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EST_ACT_PICKUP_ERR_MINUTES) AS median_pickup_min,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EST_ACT_DROPOFF_ERR_MINUTES) AS median_dropoff_min,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES) AS median_total_late_min,
        SUM(CASE WHEN (EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES) > 10 THEN 1 ELSE 0 END) AS count_over_10min_total,
        SUM(CASE WHEN (EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES) > 15 THEN 1 ELSE 0 END) AS count_over_15min_total
    FROM edw.opex.fact_dx_fraud_pc_rolling_scores
    WHERE timebased_pay_model NOT IN ('order mode')
      AND assignment_created_at >= '2025-12-10'::date
      AND assignment_created_at <= '2026-01-07'::date
      AND DELIVERY_DEVIATION_SCORE IS NOT NULL
    GROUP BY dasher_id
    HAVING COUNT(*) >= 20
),
tier3 AS (
    SELECT *,
        CASE
            WHEN median_pickup_min > 8 AND median_dropoff_min < 3 THEN 'Pickup-Heavy'
            WHEN median_dropoff_min > 8 AND median_pickup_min < 3 THEN 'Dropoff-Heavy'
            WHEN median_pickup_min >= 3 AND median_dropoff_min >= 3 THEN 'Mixed'
            ELSE 'Other'
        END AS lateness_pattern
    FROM dasher_medians
    WHERE (100.0 * count_over_10min_total / total_deliveries) > 50
      AND (100.0 * count_over_15min_total / total_deliveries) <= 50
)
SELECT
    lateness_pattern,
    COUNT(*) AS dasher_count,
    ROUND(AVG(median_pickup_min), 2) AS avg_pickup,
    ROUND(AVG(median_dropoff_min), 2) AS avg_dropoff,
    ROUND(AVG(median_total_late_min), 2) AS avg_total
FROM tier3
GROUP BY lateness_pattern
ORDER BY dasher_count DESC;
```

---

*Analysis conducted January 8, 2026*
