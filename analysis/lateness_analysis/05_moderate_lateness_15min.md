# Tier 2: Moderate Lateness Analysis

> **Analysis Date:** January 7, 2026
> **Data Source:** `edw.opex.fact_dx_fraud_pc_rolling_scores`
> **Scope:** Dashers with moderate lateness patterns (excluding Tier 1 egregious cases)
> **Lateness Metric:** Total Lateness = Pickup Lateness + Dropoff Lateness

---

## Summary

These dashers show **selective lateness patterns**. Unlike Tier 1 (egregious, constant lateness), these dashers mix on-time deliveries with significantly late ones.

### Population by Tier (using Total Lateness)

| Tier | Definition | Dasher Count |
|------|------------|--------------|
| **Tier 1: Egregious** | >50% deliveries with 30+ min total late | 14 dashers |
| **Tier 2: Moderate** | >50% over 15 min, ≤50% over 30 min total late | **77 dashers** |
| **Tier 3: Mild** | >50% over 10 min, ≤50% over 15 min total late | **329 dashers** |
| **Total at-risk** | >50% deliveries 10+ min total late | **420 dashers** |

---

## Tier 2: Moderate Lateness (>50% over 15 min, ≤50% over 30 min total late)

Top 15 Tier 2 dashers by percentage over 15 min:

| Dasher ID | Deliveries | Med Pickup | Med Dropoff | Med Total | % >15min | % >30min |
|-----------|------------|------------|-------------|-----------|----------|----------|
| F**67268112** | 31 | 31.07 min | -2.83 min | **28.45 min** | **80.6%** | 45.2% |
| U**2573909** | 60 | 18.61 min | -0.07 min | **17.59 min** | **80.0%** | 5.0% |
| **60292371** | 32 | 20.12 min | -1.43 min | **18.49 min** | **75.0%** | 3.1% |
| **29043870** | 20 | 13.30 min | 8.09 min | **26.17 min** | **75.0%** | 35.0% |
| **32402341** | 40 | 26.18 min | -0.55 min | **24.43 min** | **72.5%** | 45.0% |
| **46904950** | 21 | 11.88 min | 4.37 min | **21.62 min** | **71.4%** | 19.0% |
| **61381648** | 21 | 20.37 min | -2.23 min | **17.95 min** | **71.4%** | 9.5% |
| **7372796** | 31 | 17.43 min | 2.95 min | **21.20 min** | **71.0%** | 29.0% |
| **66405525** | 20 | 10.08 min | 7.63 min | **23.64 min** | **70.0%** | 25.0% |
| **32871454** | 126 | 18.62 min | 4.64 min | **23.95 min** | **69.8%** | 31.0% |
| **67713347** | 22 | 12.29 min | 3.68 min | **18.51 min** | **68.2%** | 22.7% |
| **47600977** | 25 | 40.28 min | -18.18 min | **23.25 min** | **68.0%** | 36.0% |
| **44128202** | 25 | 16.80 min | 2.68 min | **21.73 min** | **68.0%** | 16.0% |
| **1675750** | 41 | 27.22 min | -3.82 min | **21.93 min** | **65.9%** | 31.7% |
| **55114061** | 23 | 22.95 min | 1.27 min | **26.88 min** | **65.2%** | 47.8% |

### Key Pattern: Pickup-Heavy Lateness

Many Tier 2 dashers show a **pickup-heavy pattern**:
- Median pickup: 15-40 min late
- Median dropoff: -5 to +5 min (on-time or early)
- Total lateness driven primarily by pickup delays

### Key Pattern: Mixed Lateness

Some Tier 2 dashers show lateness spread across both pickup and dropoff:
- Median pickup: 10-15 min late
- Median dropoff: 5-10 min late
- Lower individual delays but consistent across both phases

---

## Key Difference from Tier 1

| Aspect | Tier 1 (Egregious) | Tier 2 (Moderate) |
|--------|-------------------|-------------------|
| % >30 min late | 56-94% | 3-48% |
| Median total late | 33-100 min | 17-28 min |
| Variance | High (dropoff-heavy) | Mixed patterns |
| Primary pattern | Dropoff delays | Pickup delays |

---

## SQL Queries

### Find Tier 2 Dashers (>50% over 15 min, <=50% over 30 min total late)

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
      AND assignment_created_at >= dateadd(dd,-28,current_date())
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
    ROUND(100.0 * count_over_30min_total / total_deliveries, 1) AS pct_over_30min,
    ROUND(100.0 * count_over_15min_total / total_deliveries, 1) AS pct_over_15min,
    ROUND(100.0 * count_over_10min_total / total_deliveries, 1) AS pct_over_10min
FROM dasher_medians
WHERE (100.0 * count_over_15min_total / total_deliveries) > 50  -- >50% over 15 min
  AND (100.0 * count_over_30min_total / total_deliveries) <= 50 -- Exclude Tier 1
ORDER BY pct_over_15min DESC, total_deliveries DESC;
```

### Count Dashers by Tier

```sql
WITH dasher_medians AS (
    SELECT
        dasher_id,
        COUNT(*) AS total_deliveries,
        SUM(CASE WHEN (EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES) > 30 THEN 1 ELSE 0 END) AS count_over_30min_total,
        SUM(CASE WHEN (EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES) > 15 THEN 1 ELSE 0 END) AS count_over_15min_total,
        SUM(CASE WHEN (EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES) > 10 THEN 1 ELSE 0 END) AS count_over_10min_total
    FROM edw.opex.fact_dx_fraud_pc_rolling_scores
    WHERE timebased_pay_model NOT IN ('order mode')
      AND assignment_created_at >= dateadd(dd,-28,current_date())
      AND DELIVERY_DEVIATION_SCORE IS NOT NULL
    GROUP BY dasher_id
    HAVING COUNT(*) >= 20
)
SELECT
    'Tier 1: >50% over 30 min total late' AS tier,
    COUNT(*) AS dasher_count
FROM dasher_medians
WHERE (100.0 * count_over_30min_total / total_deliveries) > 50
UNION ALL
SELECT
    'Tier 2: >50% over 15 min (excl Tier 1)' AS tier,
    COUNT(*) AS dasher_count
FROM dasher_medians
WHERE (100.0 * count_over_15min_total / total_deliveries) > 50
  AND (100.0 * count_over_30min_total / total_deliveries) <= 50
UNION ALL
SELECT
    'Tier 3: >50% over 10 min (excl Tier 1-2)' AS tier,
    COUNT(*) AS dasher_count
FROM dasher_medians
WHERE (100.0 * count_over_10min_total / total_deliveries) > 50
  AND (100.0 * count_over_15min_total / total_deliveries) <= 50;
```

---

*Analysis conducted January 7, 2026*
