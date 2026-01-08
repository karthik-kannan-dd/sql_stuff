# Lateness Analysis

Analysis of dasher lateness patterns using `edw.opex.fact_dx_fraud_pc_rolling_scores`.

**Key Metric: Total Lateness = Pickup Lateness + Dropoff Lateness**

---

## Files in this Directory

| File | Description |
|------|-------------|
| `01_table_schema.md` | Schema documentation for fact_dx_fraud_pc_rolling_scores |
| `02_l50_sum_score_deep_dive.md` | L50 Sum Score analysis with total lateness - identifies outlier vs consistent lateness |
| `03_median_based_tbpm_analysis.md` | Median-based analysis identifying time abuse patterns by tier |
| `04_tier1_egregious_deliveries.md` | Individual deliveries for Tier 1 dashers (>50% over 30 min total late) |
| `05_moderate_lateness_15min.md` | Tier 2 dashers with selective lateness patterns |
| `06_lateness_distribution_histogram.md` | Histogram: % of dashers by lateness delivery rate |
| `07_worst_dashers_by_median_lateness.md` | Top 20 worst dashers by median total lateness with sample deliveries |
| `tools/` | Streamlit lookup tool for dasher lateness |

---

## Key Methodology: Total Lateness

**Total Lateness = Pickup Lateness + Dropoff Lateness**

---

## Key Findings Summary

### Population Summary (using Total Lateness)

| Tier | Definition | Dasher Count |
|------|------------|--------------|
| **Tier 1: Egregious** | >50% deliveries with 30+ min total late | **14 dashers** |
| **Tier 2: Moderate** | >50% over 15 min, ≤50% over 30 min total late | **77 dashers** |
| **Tier 3: Mild** | >50% over 10 min, ≤50% over 15 min total late | **329 dashers** |
| **Total at-risk** | | **420 dashers** |

### Two Distinct Lateness Patterns

**1. Dropoff-Heavy**
- Early to pickup (median -2 to +5 min)
- Very late to dropoff (median 40-100 min)
- Example: Dasher 8026806 with 94% of deliveries 30+ min total late

**2. Pickup-Heavy**
- Very late to pickup (median 30-50 min)
- On-time or early to dropoff (median -10 to +5 min)
- Example: Dasher 53090914 with median 47 min pickup, -11 min dropoff

### L50 Sum Score Findings

- High L50 sum scores often driven by **single extreme outliers** (data anomalies)
- Dashers with 99% of score from one delivery are likely data issues, not abuse
- Median-based metrics are more robust for identifying consistent abuse

---

## Detection Criteria

### Recommended Flags (using Total Lateness)

| Tier | Criteria | Action |
|------|----------|--------|
| **Tier 1** | >50% deliveries with total lateness >30 min | Immediate review |
| **Tier 2** | >50% with total lateness >15 min (excl Tier 1) | Monitoring/Warning |
| **Tier 3** | >50% with total lateness >10 min (excl Tier 1-2) | Pattern tracking |

### Additional Signal: Pattern Type

| Pattern | Detection | Implication |
|---------|-----------|-------------|
| Dropoff-Heavy | Med pickup < 5 min, Med dropoff > 30 min | Delay during delivery |
| Pickup-Heavy | Med pickup > 20 min, Med dropoff < 10 min | Hold at restaurant |

---

## Recommendations

1. **Use Total Lateness** as primary metric for TBPM abuse detection
2. **Review Tier 1 dashers (14 total)** for immediate intervention
3. **Monitor Tier 2 dashers (77 total)** for pattern escalation
4. **Track both pickup and dropoff** separately to identify pattern type
5. **Exclude data outliers** (single deliveries with >100 deviation score) from aggregate metrics

---

## Source Tables

- `edw.opex.fact_dx_fraud_pc_rolling_scores` - Primary lateness/deviation scores
- Key columns:
  - `EST_ACT_PICKUP_ERR_MINUTES` - Pickup lateness
  - `EST_ACT_DROPOFF_ERR_MINUTES` - Dropoff lateness
  - `DELIVERY_DEVIATION_SCORE` - Per-delivery deviation score
  - `DELIVERY_DEVIATION_SCORE_SUM_L50_TBPM` - Rolling sum of last 50 TBPM scores

---

*Updated: January 7, 2026*
