# Tier 1: Egregious Lateness - Individual Deliveries

> **Analysis Date:** January 7, 2026
> **Data Source:** `edw.opex.fact_dx_fraud_pc_rolling_scores`
> **Scope:** Individual deliveries for dashers with >50% deliveries 30+ min total late
> **Lateness Metric:** Total Lateness = Pickup Lateness + Dropoff Lateness

---

## Summary

These 14 dashers show **constant, extreme lateness** on virtually every delivery:
- **56-94% of deliveries have total lateness >30 minutes**
- Median total lateness: **33-100 minutes**
- Three patterns: Dropoff-Heavy, Pickup-Heavy, and Mixed

| Dasher ID | Deliveries | % >30min Total | Med Pickup | Med Dropoff | Med Total | Pattern |
|-----------|------------|----------------|------------|-------------|-----------|---------|
| **8026806** | 110 | **93.6%** | -2.17 min | 101.46 min | **99.39 min** | Dropoff-Heavy |
| **65023622** | 87 | **92.0%** | -2.72 min | 102.32 min | **99.52 min** | Dropoff-Heavy |
| **67706906** | 22 | **86.4%** | 5.05 min | 46.74 min | **88.77 min** | Dropoff-Heavy |
| **57134452** | 120 | **84.2%** | -1.50 min | 96.12 min | **98.38 min** | Dropoff-Heavy |
| **67754477** | 25 | **80.0%** | 4.68 min | 51.18 min | **79.60 min** | Dropoff-Heavy |
| **67433810** | 28 | **78.6%** | 1.58 min | 45.54 min | **53.91 min** | Dropoff-Heavy |
| **67482992** | 22 | **77.3%** | 2.61 min | 69.76 min | **88.40 min** | Dropoff-Heavy |
| **67482904** | 21 | **76.2%** | 1.70 min | 42.35 min | **60.85 min** | Dropoff-Heavy |
| **67086725** | 39 | **71.8%** | 4.18 min | 45.83 min | **57.38 min** | Dropoff-Heavy |
| **36963906** | 40 | **65.0%** | -2.89 min | 99.78 min | **96.24 min** | Dropoff-Heavy |
| **67086507** | 31 | **64.5%** | 1.25 min | 48.78 min | **49.15 min** | Dropoff-Heavy |
| **35560585** | 54 | **59.3%** | 12.36 min | 16.79 min | **33.73 min** | **Mixed** |
| **66919671** | 58 | **58.6%** | **38.02 min** | -2.66 min | **36.63 min** | **Pickup-Heavy** |
| **53090914** | 62 | **56.5%** | **46.95 min** | -11.48 min | **36.24 min** | **Pickup-Heavy** |

---

## Dasher 8026806 (110 deliveries, 93.6% >30min total late)

**Pattern:** Dropoff-Heavy - arrives early to pickup, delivers extremely late

| Date | Delivery ID | Pickup | Dropoff | Total Late |
|------|-------------|--------|---------|------------|
| 2025-12-30 | 3198770049 | -4.7 min | 104.9 min | **100.2 min** |
| 2025-12-30 | 2727310426 | -2.8 min | 105.1 min | **102.3 min** |
| 2025-12-30 | 3123839632 | -7.7 min | 106.9 min | **99.2 min** |
| 2025-12-30 | 2502833477 | -4.5 min | 103.9 min | **99.4 min** |
| 2025-12-30 | 3257943064 | -2.5 min | 38.4 min | **35.9 min** |
| 2025-12-30 | 2885534743 | 21.9 min | 85.7 min | **107.6 min** |
| 2025-12-29 | 2050505943 | -5.7 min | 101.5 min | **95.7 min** |
| 2025-12-29 | 3308042151 | -2.3 min | 110.9 min | **108.6 min** |
| 2025-12-29 | 2528351459 | -4.0 min | 0.4 min | -3.6 min |
| 2025-12-29 | 3445531437 | -2.2 min | 106.1 min | **103.9 min** |
| 2025-12-29 | 2535066912 | -4.0 min | 107.4 min | **103.4 min** |
| 2025-12-29 | 2891183956 | -0.9 min | 83.5 min | **82.6 min** |
| 2025-12-29 | 2587255324 | -2.0 min | 334.7 min | **332.6 min** |
| 2025-12-29 | 2468414191 | 31.6 min | 72.4 min | **104.1 min** |
| 2025-12-28 | 2252574675 | -1.4 min | 116.2 min | **114.9 min** |

**Observations:**
- 14 of 15 deliveries shown have total lateness >30 min (93%)
- Most extreme: **332.6 min total late** (5.5 hours!)
- Classic pattern: Early pickup (-5 to +5 min), Late dropoff (80-335 min)

---

## Pickup-Heavy Pattern Dashers

**These dashers show a different pattern - primarily delayed at pickup.**

| Dasher ID | Med Pickup | Med Dropoff | Med Total | % >30min |
|-----------|------------|-------------|-----------|----------|
| **66919671** | **38.02 min late** | -2.66 min (early) | **36.63 min** | **58.6%** |
| **53090914** | **46.95 min late** | -11.48 min (early) | **36.24 min** | **56.5%** |


---

## SQL Query Used

```sql
-- Get individual deliveries with total lateness for Tier 1 dashers
SELECT
    dasher_id,
    delivery_id,
    assignment_created_at::date AS delivery_date,
    ROUND(EST_ACT_PICKUP_ERR_MINUTES, 1) AS pickup_late_min,
    ROUND(EST_ACT_DROPOFF_ERR_MINUTES, 1) AS dropoff_late_min,
    ROUND(EST_ACT_PICKUP_ERR_MINUTES + EST_ACT_DROPOFF_ERR_MINUTES, 1) AS total_late_min
FROM edw.opex.fact_dx_fraud_pc_rolling_scores
WHERE dasher_id IN (8026806, 65023622, 67706906, 57134452, 67754477, 67433810, 67482992, 67482904, 67086725, 36963906, 67086507, 35560585, 66919671, 53090914)
  AND timebased_pay_model NOT IN ('order mode')
  AND assignment_created_at >= dateadd(dd,-28,current_date())
ORDER BY dasher_id, assignment_created_at DESC;
```

---

*Analysis conducted January 7, 2026*
