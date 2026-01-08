# Geospoofing Analysis: Completion Filter Changes

**Date:** 2026-01-06

## Overview

All geospoofing analysis queries have been updated to join with `DIMENSION_DELIVERIES` table to ensure we only flag dashers who actually completed the delivery (not intermediate dashers who were reassigned mid-delivery).

## Key Changes

### Join Logic Added
```sql
INNER JOIN PRODDB.PUBLIC.DIMENSION_DELIVERIES dd
    ON gps.DELIVERY_UUID = dd.DELIVERY_UUID
    AND gps.DASHER_ID = dd.DASHER_ID  -- GPS dasher must match completing dasher
WHERE ...
  AND dd.ACTIVE_DATE >= DATEADD(day, -3, CURRENT_DATE())  -- Date filter for performance
  AND dd.ACTUAL_DELIVERY_TIME IS NOT NULL  -- Only completed deliveries
```

### Filters Applied
1. **ACTUAL_DELIVERY_TIME IS NOT NULL**: Only includes deliveries that were actually completed (dropped off)
2. **gps.DASHER_ID = dd.DASHER_ID**: GPS data from the completing dasher only
3. **ACTIVE_DATE filter**: Required for DIMENSION_DELIVERIES performance (massive table)

---

## Impact on Results

### Total Flagged Deliveries (3-day)

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Total flagged deliveries | 6,064 | 1,034 | -83% |
| Unique dashers flagged | 5,388 | 716 | -87% |

### Interpretation
- **~83% reduction** in flagged deliveries
- Many original flags were from dashers who had GPS data but were reassigned before completion
- Remaining flags are more accurate - these are dashers who actually completed deliveries with suspicious GPS patterns

### Repeat Offenders (Top 5)

| Dasher ID | Before | After | Change |
|-----------|--------|-------|--------|
| 68143350  | 53     | 52    | -1     |
| 67938948  | 42     | 42    | 0      |
| 67951383  | 42     | 41    | -1     |
| 67924959  | 42     | 42    | 0      |
| 67938676  | 41     | 41    | 0      |

### Interpretation
- Top repeat offenders largely unchanged (confirming they actually completed flagged deliveries)
- These dashers are legitimate spoofing suspects

---

## Files Updated

1. **static_course_altitude.md**
   - All 4 queries updated with completion filter
   - Results refreshed with new data

2. **dasher_samples.md**
   - High count dasher queries updated
   - Low count dasher queries updated

3. **low_ping_count_deliveries.md**
   - Main query updated with completion filter

---

## Rationale

Before this change, the analysis could flag the wrong dashers because:
1. Delivery gets assigned to Dasher A
2. Dasher A has suspicious GPS patterns
3. Delivery gets reassigned to Dasher B
4. Dasher B completes the delivery legitimately
5. **Old analysis**: Flags Dasher A (incorrect - they didn't complete it)
6. **New analysis**: Only flags if completing dasher (from DIMENSION_DELIVERIES) has suspicious GPS patterns

---

## Performance Notes

- DIMENSION_DELIVERIES is a massive table - always filter by `ACTIVE_DATE`
- Queries may take longer due to the join (20-30 minutes is normal)
- Results are more accurate but sample sizes are smaller

