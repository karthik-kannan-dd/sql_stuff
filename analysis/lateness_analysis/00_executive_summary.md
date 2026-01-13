# Lateness Analysis - Executive Summary

## Analysis Parameters

| Parameter | Value |
|-----------|-------|
| Analysis Date | January 7-8, 2026 |
| Data Period | December 10, 2025 - January 7, 2026 |
| Lookback Window | 28 days |
| Key Metric | Total Lateness = Pickup Lateness + Dropoff Lateness |
| Data Source | edw.opex.fact_dx_fraud_pc_rolling_scores |

---

## Key Talking Points

### 1. The vast majority of dashers are on-time
- 64.7% of dashers have 5% or fewer late deliveries (>10 min)
- 13.8% of dashers have zero late deliveries
- Both Order Mode and TBPM dashers are generally early (median -2 to -5 min)

### 2. Late delivery rates are nearly identical across pay models
- Order Mode: 4.34% deliveries >10 min late
- TBPM: 4.32% deliveries >10 min late
- The difference is negligible (~0.5 min median difference)

### 3. Only 420 dashers (0.16%) show persistent lateness patterns
- Tier 1 (Egregious): 14 dashers - >50% deliveries 30+ min total late
- Tier 2 (Moderate): 77 dashers - >50% deliveries 15+ min total late
- Tier 3 (Mild): 329 dashers - >50% deliveries 10+ min total late

### 4. Distinct lateness patterns exist by tier
| Tier | Primary Pattern | Typical Behavior |
|------|-----------------|------------------|
| Tier 1 | Dropoff-Heavy | Early pickup (-2 to +5 min), very late dropoff (40-100 min) |
| Tier 2 | Pickup-Heavy | Late pickup (15-40 min), on-time dropoff |
| Tier 3 | Mixed | Moderate delays split across pickup and dropoff |

### 5. L50 sum scores can be misleading
- High aggregate scores are often driven by single extreme outliers (data anomalies)
- Median-based metrics are more robust for identifying consistent lateness patterns
- Example: A dasher with a 1,775 L50 sum score had 99% of that from a single delivery

### 6. Regional TBPM variation exists
| Pay Model | Median Total Late | % >10min Late |
|-----------|-------------------|---------------|
| CA Topup (Best) | -1.97 min | 2.79% |
| Order Mode | -1.97 min | 4.34% |
| TimeMode | -0.70 min | 6.25% |
| SEA Topup (Worst) | +0.02 min | 8.69% |

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total dashers analyzed | 269,851 |
| Total deliveries analyzed | 34.2M |
| Dashers with 0% late deliveries | 37,259 (13.8%) |
| Dashers with >50% late deliveries | 420 (0.16%) |

---

## Methodology Notes

- Late threshold: >10 minutes total lateness (pickup + dropoff combined)
- Minimum sample: 20+ TBPM deliveries per dasher
- Positive lateness = late, negative lateness = early
- Used median-based approach to avoid outlier bias

---

*Updated: January 2026*
