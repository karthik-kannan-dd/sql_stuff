# Lateness Analysis

Analysis of dasher lateness patterns using `edw.opex.fact_dx_fraud_pc_rolling_scores`.

**Analysis Period:** December 10, 2025 - January 7, 2026
**Key Metric:** Total Lateness = Pickup Lateness + Dropoff Lateness

---

## Files in this Directory

| File | Description |
|------|-------------|
| `01_lateness_distribution.md` | Histogram showing % of dashers by lateness delivery rate |
| `02_order_mode_vs_tbpm.md` | Comparison of lateness across pay models (order mode vs TBPM variants) |
| `03_l50_vs_median_methodology.md` | L50 Sum Score vs median-based methodology - identifies outlier vs consistent lateness |
| `04_tier_definitions.md` | Tier definitions and criteria using total lateness metric |
| `05_tier1_egregious.md` | Tier 1: Egregious dashers (>50% deliveries 30+ min total late) - 14 dashers |
| `06_tier2_moderate.md` | Tier 2: Moderate dashers (>50% over 15 min, ≤50% over 30 min) - 77 dashers |
| `06a_deep_dive_dasher_32402341.md` | Deep dive: Store wait time validation for Tier 2 dasher |
| `07_tier3_mild.md` | Tier 3: Mild dashers (>50% over 10 min, ≤50% over 15 min) - 329 dashers |
| `tools/` | Streamlit lookup tool for dasher lateness |

---

## Population Summary

| Tier | Definition | Dasher Count |
|------|------------|--------------|
| **Tier 1: Egregious** | >50% deliveries with 30+ min total late | 14 dashers |
| **Tier 2: Moderate** | >50% over 15 min, ≤50% over 30 min total late | 77 dashers |
| **Tier 3: Mild** | >50% over 10 min, ≤50% over 15 min total late | 329 dashers |
| **Total at-risk** | >50% deliveries 10+ min total late | **420 dashers** |

---

## Key Findings

### Lateness Patterns by Tier

**Tier 1 (Egregious):** Primarily dropoff-heavy pattern
- Early to pickup (median -2 to +5 min)
- Very late to dropoff (median 40-100 min)

**Tier 2 (Moderate):** Primarily pickup-heavy pattern
- Late to pickup (median 15-40 min)
- On-time or early to dropoff (median -5 to +5 min)

**Tier 3 (Mild):** Mixed patterns
- 43% pickup-heavy, 39% mixed, 17% other, 2% dropoff-heavy

### Pay Model Comparison

Both order mode and TBPM dashers are generally early on deliveries. Key differences:
- **Median total lateness:** Order mode -2.50 min, TBPM (excl order mode) -4.95 min
- **75th percentile:** Order mode +2.72 min, TBPM +2.16 min
- CA Topup shows the best performance; SEA Topup shows the worst among TBPM variants

### Methodology Finding

L50 sum scores can be driven by single extreme outliers (data anomalies). Median-based metrics are more robust for identifying consistent patterns.

---

## Source Tables

- `edw.opex.fact_dx_fraud_pc_rolling_scores` - Primary lateness/deviation scores
- `edw.opex.fact_dx_fraud_assignment` - Assignment-level data including store wait times
- `proddb.public.dimension_deliveries` - Store info, delivery details

### Key Columns

| Column | Description |
|--------|-------------|
| `EST_ACT_PICKUP_ERR_MINUTES` | Pickup lateness (positive = late) |
| `EST_ACT_DROPOFF_ERR_MINUTES` | Dropoff lateness (positive = late) |
| `MX_ARRIVAL_TO_PICKUP_SECOND` | Store wait time in seconds |
| `DASHER_CONFIRMED_STORE_ARRIVAL_TIME` | When dasher arrived at store |

---

*Updated: January 7, 2026*
