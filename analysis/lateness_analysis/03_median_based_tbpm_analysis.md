# Median-Based Analysis: Consistently Late TBPM Dashers

> **Analysis Date:** January 7, 2026
> **Data Source:** `edw.opex.fact_dx_fraud_pc_rolling_scores`
> **Scope:** Dashers with 20+ TBPM deliveries in last 28 days
> **Lateness Metric:** Total Lateness = Pickup Lateness + Dropoff Lateness

---

## Executive Summary

Using a **median-based approach** with **Total Lateness** (pickup + dropoff), we identified dashers who are **consistently late across all deliveries** rather than having high scores due to single extreme events.

### Population Summary

| Tier | Definition | Dasher Count |
|------|------------|--------------|
| **Tier 1: Egregious** | >50% deliveries with 30+ min total late | **14 dashers** |
| **Tier 2: Moderate** | >50% deliveries with 15+ min total late (excl Tier 1) | **77 dashers** |
| **Tier 3: Mild** | >50% deliveries with 10+ min total late (excl Tier 1-2) | **329 dashers** |

**Total: 420 dashers** with significant lateness patterns (20+ deliveries each).

---

## Tier 1: Egregious Lateness (>50% deliveries 30+ min total late)

These dashers are consistently late on the majority of their deliveries.

| Dasher ID | Deliveries | Med Pickup | Med Dropoff | Med Total Late | % >30min |
|-----------|------------|------------|-------------|----------------|----------|
| **8026806** | 110 | -2.17 min | 101.46 min | **99.39 min** | **93.6%** |
| **65023622** | 87 | -2.72 min | 102.32 min | **99.52 min** | **92.0%** |
| **67706906** | 22 | 5.05 min | 46.74 min | **88.77 min** | **86.4%** |
| **57134452** | 120 | -1.50 min | 96.12 min | **98.38 min** | **84.2%** |
| **67754477** | 25 | 4.68 min | 51.18 min | **79.60 min** | **80.0%** |
| **67433810** | 28 | 1.58 min | 45.54 min | **53.91 min** | **78.6%** |
| **67482992** | 22 | 2.61 min | 69.76 min | **88.40 min** | **77.3%** |
| **67482904** | 21 | 1.70 min | 42.35 min | **60.85 min** | **76.2%** |
| **67086725** | 39 | 4.18 min | 45.83 min | **57.38 min** | **71.8%** |
| **36963906** | 40 | -2.89 min | 99.78 min | **96.24 min** | **65.0%** |
| **67086507** | 31 | 1.25 min | 48.78 min | **49.15 min** | **64.5%** |
| **35560585** | 54 | 12.36 min | 16.79 min | **33.73 min** | **59.3%** |
| **66919671** | 58 | **38.02 min** | -2.66 min | **36.63 min** | **58.6%** |
| **53090914** | 62 | **46.95 min** | -11.48 min | **36.24 min** | **56.5%** |

### Two Distinct Patterns in Tier 1

**Pattern A: Dropoff-Heavy (10 dashers)**
- Arrive **EARLY to pickup** (median -3 to +5 min)
- Very **late to dropoff** (median 42-102 min)
- Pick up food promptly, significant delay during delivery phase

**Pattern B: Pickup-Heavy (2 dashers)**
- **Dasher 66919671**: Median pickup 38 min late, median dropoff -2.7 min
- **Dasher 53090914**: Median pickup 47 min late, median dropoff -11.5 min

**Pattern C: Mixed (2 dashers)**
- **Dasher 35560585**: 12 min pickup late, 17 min dropoff late - lateness spread across both

---

## SQL Queries

### Query 1: Find Consistently Late Dashers by Tier (Total Lateness)

```sql
WITH dasher_medians AS (
    SELECT
        dasher_id,
        COUNT(*) AS total_deliveries,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY DELIVERY_DEVIATION_SCORE) AS median_deviation_score,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EST_ACT_PICKUP_ERR_MINUTES) AS median_pickup_min,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EST_ACT_DROPOFF_ERR_MINUTES) AS median_dropoff_min,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES) AS median_total_late_min,
        SUM(CASE WHEN (EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES) > 30 THEN 1 ELSE 0 END) AS count_over_30min_total,
        SUM(CASE WHEN (EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES) > 15 THEN 1 ELSE 0 END) AS count_over_15min_total,
        MAX(DELIVERY_DEVIATION_SCORE) AS max_single_score
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
    ROUND(median_deviation_score, 2) AS median_dev_score,
    ROUND(median_pickup_min, 2) AS median_pickup_min,
    ROUND(median_dropoff_min, 2) AS median_dropoff_min,
    ROUND(median_total_late_min, 2) AS median_total_late_min,
    count_over_30min_total,
    ROUND(100.0 * count_over_30min_total / total_deliveries, 1) AS pct_over_30min_total,
    count_over_15min_total,
    ROUND(100.0 * count_over_15min_total / total_deliveries, 1) AS pct_over_15min_total
FROM dasher_medians
WHERE (100.0 * count_over_30min_total / total_deliveries) > 50  -- Tier 1
ORDER BY pct_over_30min_total DESC, total_deliveries DESC;
```

### Query 2: Count Dashers by Tier

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
