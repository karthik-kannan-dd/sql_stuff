# Strict Spoofing Signature Detection

**Objective:** Identify deliveries with the Android spoofing signature: `altitude = 2.0`

**Important:** All queries join with `DIMENSION_DELIVERIES` to ensure we only flag the dasher who actually completed the delivery.

---

## Comparison: Strict vs General Filter

| Filter | Deliveries | Dashers | Avg Deliveries/Dasher |
|--------|------------|---------|----------------------|
| Static course/altitude (any value) | 1,034 | 716 | 1.44 |
| **`altitude = 2.0`** | **342** | **11** | **31.1** |

**Key Insight:** The strict filter reduces flagged deliveries by 67% and dashers by 98%, but the remaining 11 dashers average 31 flagged deliveries each - clear repeat offenders.

---

## Query: Total Flagged Deliveries (Strict Signature)

```sql
SELECT
    COUNT(DISTINCT DELIVERY_UUID) as total_flagged_deliveries,
    COUNT(DISTINCT DASHER_ID) as unique_dashers
FROM (
    SELECT
        gps.DASHER_ID,
        gps.DELIVERY_UUID
    FROM proddb.public.dimension_dasher_location_enhanced gps
    INNER JOIN PRODDB.PUBLIC.DIMENSION_DELIVERIES dd
        ON gps.DELIVERY_UUID = dd.DELIVERY_UUID
        AND gps.DASHER_ID = dd.DASHER_ID
    WHERE gps.TIME >= DATEADD(day, -3, CURRENT_TIMESTAMP())
      AND gps.DELIVERY_UUID IS NOT NULL
      AND dd.ACTIVE_DATE >= DATEADD(day, -3, CURRENT_DATE())
      AND dd.ACTUAL_DELIVERY_TIME IS NOT NULL
    GROUP BY gps.DASHER_ID, gps.DELIVERY_UUID
    HAVING
        MIN(gps.COURSE) = MAX(gps.COURSE)
        AND MIN(gps.ALTITUDE) = MAX(gps.ALTITUDE)
        AND MIN(gps.ALTITUDE) = 2.0
        AND COUNT(*) >= 5
);
```

### Results (Run: 2026-01-06, last 3 days)

| TOTAL_FLAGGED_DELIVERIES | UNIQUE_DASHERS |
|--------------------------|----------------|
| 342                      | 11             |

---

## Query: Repeat Offenders (Strict Signature)

```sql
SELECT
    gps.DASHER_ID,
    COUNT(DISTINCT gps.DELIVERY_UUID) as flagged_deliveries,
    SUM(ping_count) as total_pings
FROM (
    SELECT
        gps.DASHER_ID,
        gps.DELIVERY_UUID,
        COUNT(*) as ping_count
    FROM proddb.public.dimension_dasher_location_enhanced gps
    INNER JOIN PRODDB.PUBLIC.DIMENSION_DELIVERIES dd
        ON gps.DELIVERY_UUID = dd.DELIVERY_UUID
        AND gps.DASHER_ID = dd.DASHER_ID
    WHERE gps.TIME >= DATEADD(day, -3, CURRENT_TIMESTAMP())
      AND gps.DELIVERY_UUID IS NOT NULL
      AND dd.ACTIVE_DATE >= DATEADD(day, -3, CURRENT_DATE())
      AND dd.ACTUAL_DELIVERY_TIME IS NOT NULL
    GROUP BY gps.DASHER_ID, gps.DELIVERY_UUID
    HAVING
        MIN(gps.COURSE) = MAX(gps.COURSE)
        AND MIN(gps.ALTITUDE) = MAX(gps.ALTITUDE)
        AND MIN(gps.ALTITUDE) = 2.0
        AND COUNT(*) >= 5
) gps
GROUP BY gps.DASHER_ID
ORDER BY flagged_deliveries DESC
LIMIT 20;
```

### Results (Run: 2026-01-06, last 3 days)

| DASHER_ID | FLAGGED_DELIVERIES | TOTAL_PINGS |
|-----------|-------------------|-------------|
| 68143350  | 54                | 30,855      |
| 67924959  | 42                | 1,857       |
| 67938948  | 42                | 1,794       |
| 67938676  | 41                | 1,654       |
| 67951383  | 41                | 1,903       |
| 68143525  | 40                | 1,848       |
| 68143616  | 36                | 1,515       |
| 68038246  | 17                | 9,353       |
| 68172153  | 14                | 8,655       |
| 68012711  | 14                | 7,794       |
| 28886845  | 1                 | 368         |

### Observations

1. **Top offender**: Dasher 68143350 has **54 flagged deliveries** with 30,855 total pings - extremely high confidence spoofing

2. **Cluster of similar IDs**: Five dashers (67924959, 67938948, 67951383, 67938676, 68143525) all have 40-42 flagged deliveries
   - Sequential dasher IDs suggest coordinated sign-ups
   - Similar ping counts (~1,650-1,900) suggest same spoofing tool/behavior

3. **Two tiers of offenders**:
   - **Tier 1** (36-54 deliveries): 7 dashers - systematic, daily spoofing
   - **Tier 2** (14-17 deliveries): 3 dashers - still significant but less frequent

4. **Ping count patterns**:
   - High ping counts (7,000-30,000): Prolonged spoofing sessions
   - Low ping counts (~1,600-1,900): Shorter delivery windows, rapid-fire pattern

---

## Query: Sample Deliveries (Strict Signature)

```sql
SELECT
    gps.DELIVERY_UUID,
    gps.DASHER_ID,
    COUNT(*) as ping_count,
    MIN(gps.COURSE) as course,
    MIN(gps.ALTITUDE) as altitude,
    MIN(gps.LAT) as lat,
    MIN(gps.LNG) as lng,
    MIN(gps.TIME) as first_ping,
    MAX(gps.TIME) as last_ping,
    MAX(gps.DEVICE_TYPE) as device_type
FROM proddb.public.dimension_dasher_location_enhanced gps
INNER JOIN PRODDB.PUBLIC.DIMENSION_DELIVERIES dd
    ON gps.DELIVERY_UUID = dd.DELIVERY_UUID
    AND gps.DASHER_ID = dd.DASHER_ID
WHERE gps.TIME >= DATEADD(day, -3, CURRENT_TIMESTAMP())
  AND gps.DELIVERY_UUID IS NOT NULL
  AND dd.ACTIVE_DATE >= DATEADD(day, -3, CURRENT_DATE())
  AND dd.ACTUAL_DELIVERY_TIME IS NOT NULL
GROUP BY gps.DELIVERY_UUID, gps.DASHER_ID
HAVING
    MIN(gps.COURSE) = MAX(gps.COURSE)
    AND MIN(gps.ALTITUDE) = MAX(gps.ALTITUDE)
    AND MIN(gps.ALTITUDE) = 2.0
    AND COUNT(*) >= 5
ORDER BY ping_count DESC
LIMIT 10;
```

### Results (Run: 2026-01-06, last 3 days)

| DELIVERY_UUID | DASHER_ID | PING_COUNT | COURSE | ALTITUDE | LAT | LNG | FIRST_PING | LAST_PING | DEVICE |
|---------------|-----------|------------|--------|----------|-----|-----|------------|-----------|--------|
| daa63108-da24-3001-b73f-5cf591128e25 | 68143350 | 1977 | 0.0 | 2.0 | 42.99 | -88.01 | 2026-01-04 09:00:59 | 2026-01-04 09:42:56 | android |
| 6833414f-21d8-3001-87b0-b4a0809e7a17 | 68143350 | 1462 | 0.0 | 2.0 | 43.00 | -87.98 | 2026-01-04 07:29:10 | 2026-01-04 08:00:16 | android |
| 5a539264-c042-3001-98c5-e219b5b63d28 | 68143350 | 1406 | 0.0 | 2.0 | 42.92 | -88.03 | 2026-01-04 10:03:09 | 2026-01-04 10:31:35 | android |
| 210f1e23-acfd-3001-bd4c-a6940e3f9d91 | 68143350 | 1395 | 0.0 | 2.0 | 42.99 | -88.04 | 2026-01-04 07:00:32 | 2026-01-04 07:28:47 | android |
| 967553d8-6920-3001-9752-fba2dd08d7f5 | 68143350 | 1253 | 0.0 | 2.0 | 42.92 | -88.02 | 2026-01-04 10:31:36 | 2026-01-04 10:56:48 | android |
| b8b94e59-4c20-3001-aaed-ca324299e465 | 68017527 | 1176 | 1.0 | 2.0 | 39.20 | -76.71 | 2026-01-03 07:45:58 | 2026-01-03 08:09:20 | android |
| 30d28417-90a6-3001-a2b2-9785af29527c | 68143350 | 1033 | 0.0 | 2.0 | 42.88 | -88.05 | 2026-01-04 01:17:04 | 2026-01-04 01:37:41 | android |
| ae5a874b-0563-3001-9378-fb4eab7bd42f | 68143350 | 998 | 0.0 | 2.0 | 42.99 | -88.03 | 2026-01-04 09:42:57 | 2026-01-04 10:03:08 | android |
| 7107be5e-7bbf-3001-a6dd-a0ac6d55e4cd | 68017527 | 924 | 1.0 | 2.0 | 39.19 | -76.69 | 2026-01-03 09:02:01 | 2026-01-03 09:20:13 | android |
| d758ef1f-4469-3001-b07a-b9422acddca8 | 68143350 | 833 | 0.0 | 2.0 | 42.89 | -88.01 | 2026-01-04 01:00:22 | 2026-01-04 01:17:02 | android |

### Observations

1. **100% Android devices** - No iOS devices with this exact signature
2. **Dasher 68143350 dominates**: 8 of top 10 deliveries by ping count
3. **Geographic clusters**:
   - Wisconsin (lat ~42.9, lng ~-88.0) - Dasher 68143350
   - Maryland (lat ~39.2, lng ~-76.7) - Dasher 68017527
4. **Long durations**: 20-42 minute deliveries with static GPS - impossible without spoofing

---

## Summary

| Metric | Value |
|--------|-------|
| Total flagged deliveries (3 days) | 342 |
| Unique dashers flagged | 11 |
| Top repeat offender | Dasher 68143350 (54 deliveries) |
| All flagged devices | Android (100%) |
| Avg flagged deliveries per dasher | 31.1 |

---

## Detection Signature

```sql
-- Strict spoofing signature detection
HAVING
    MIN(gps.COURSE) = MAX(gps.COURSE)
    AND MIN(gps.ALTITUDE) = MAX(gps.ALTITUDE)
    AND MIN(gps.ALTITUDE) = 2.0         -- Common spoofing app default
    AND COUNT(*) >= 5                   -- Minimum ping threshold
```

---

## Recommendation

These 11 dashers should be investigated with high priority:
1. **68143350** - Top offender, 54 deliveries in 3 days with spoofed GPS
2. **67924959, 67938948, 67951383, 67938676, 68143525** - Cluster with similar IDs, likely coordinated
3. **68143616** - 36 flagged deliveries
4. **68038246, 68172153, 68012711** - Tier 2 offenders with 14-17 flagged deliveries each
5. **28886845** - Single flagged delivery (possible one-time use)


