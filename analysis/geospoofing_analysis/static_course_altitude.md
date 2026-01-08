# Static Course & Altitude Detection

**Objective:** Identify deliveries where GPS course and altitude remained unchanged across all pings - a potential indicator of geospoofing.

**Rationale:** Legitimate GPS readings naturally vary in course (direction) and altitude due to movement and GPS drift. Static values across many pings suggest artificial/spoofed coordinates.

**Important:** All queries join with `DIMENSION_DELIVERIES` to ensure we only flag the dasher who actually completed the delivery (not dashers who were reassigned mid-delivery).

## Query: Sample deliveries with unchanged course & altitude

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
    AND COUNT(*) >= 5
ORDER BY ping_count DESC
LIMIT 10;
```

### Results (Run: 2026-01-06, last 3 days)

| DELIVERY_UUID | DASHER_ID | PING_COUNT | COURSE | ALTITUDE | LAT | LNG | FIRST_PING | LAST_PING | DEVICE |
|---------------|-----------|------------|--------|----------|-----|-----|------------|-----------|--------|
| daa63108-da24-3001-b73f-5cf591128e25 | 68143350 | 1977 | 0.0 | 2.0 | 42.9968 | -88.0158 | 2026-01-04 09:00:59 | 2026-01-04 09:42:56 | android |
| 6833414f-21d8-3001-87b0-b4a0809e7a17 | 68143350 | 1462 | 0.0 | 2.0 | 43.0024 | -87.9833 | 2026-01-04 07:29:10 | 2026-01-04 08:00:16 | android |
| 5a539264-c042-3001-98c5-e219b5b63d28 | 68143350 | 1406 | 0.0 | 2.0 | 42.9242 | -88.0338 | 2026-01-04 10:03:09 | 2026-01-04 10:31:35 | android |
| 210f1e23-acfd-3001-bd4c-a6940e3f9d91 | 68143350 | 1395 | 0.0 | 2.0 | 42.9922 | -88.0493 | 2026-01-04 07:00:32 | 2026-01-04 07:28:47 | android |
| 967553d8-6920-3001-9752-fba2dd08d7f5 | 68143350 | 1253 | 0.0 | 2.0 | 42.9242 | -88.0241 | 2026-01-04 10:31:36 | 2026-01-04 10:56:48 | android |
| f422be59-9441-3001-8cf7-fad1e9424927 | 60577662 | 1204 | 67.3 | 47.0 | 37.6523 | -77.6181 | 2026-01-04 11:48:07 | 2026-01-04 12:11:10 | android |
| b8b94e59-4c20-3001-aaed-ca324299e465 | 68017527 | 1176 | 1.0 | 2.0 | 39.2065 | -76.7191 | 2026-01-03 07:45:58 | 2026-01-03 08:09:20 | android |
| 30d28417-90a6-3001-a2b2-9785af29527c | 68143350 | 1033 | 0.0 | 2.0 | 42.8818 | -88.0591 | 2026-01-04 01:17:04 | 2026-01-04 01:37:41 | android |
| ae5a874b-0563-3001-9378-fb4eab7bd42f | 68143350 | 998 | 0.0 | 2.0 | 42.9921 | -88.0338 | 2026-01-04 09:42:57 | 2026-01-04 10:03:08 | android |
| 7107be5e-7bbf-3001-a6dd-a0ac6d55e4cd | 68017527 | 924 | 1.0 | 2.0 | 39.1983 | -76.6913 | 2026-01-03 09:02:01 | 2026-01-03 09:20:13 | android |

### Observations

1. **Suspiciously round values**: Most flagged deliveries have `course=0.0` and `altitude=2.0` - these are clearly artificial values
2. **Top offender dominates**: 7 of the top 10 deliveries belong to Dasher 68143350
3. **Pattern**: All Android devices, consistent `course=0.0, altitude=2.0` signature

---

## Query: Flagged Deliveries by Day

```sql
SELECT
    DATE(first_ping) as date,
    COUNT(*) as flagged_deliveries,
    COUNT(DISTINCT DASHER_ID) as unique_dashers
FROM (
    SELECT
        gps.DASHER_ID,
        gps.DELIVERY_UUID,
        MIN(gps.TIME) as first_ping
    FROM proddb.public.dimension_dasher_location_enhanced gps
    INNER JOIN PRODDB.PUBLIC.DIMENSION_DELIVERIES dd
        ON gps.DELIVERY_UUID = dd.DELIVERY_UUID
        AND gps.DASHER_ID = dd.DASHER_ID
    WHERE gps.TIME >= DATEADD(day, -7, CURRENT_TIMESTAMP())
      AND gps.DELIVERY_UUID IS NOT NULL
      AND dd.ACTIVE_DATE >= DATEADD(day, -7, CURRENT_DATE())
      AND dd.ACTUAL_DELIVERY_TIME IS NOT NULL
    GROUP BY gps.DASHER_ID, gps.DELIVERY_UUID
    HAVING
        MIN(gps.COURSE) = MAX(gps.COURSE)
        AND MIN(gps.ALTITUDE) = MAX(gps.ALTITUDE)
        AND COUNT(*) >= 5
)
GROUP BY DATE(first_ping)
ORDER BY date DESC;
```

### Results (Run: 2026-01-06, last 7 days)

| DATE       | FLAGGED_DELIVERIES | UNIQUE_DASHERS |
|------------|-------------------|----------------|
| 2026-01-04 | 536               | 318            |
| 2026-01-03 | 702               | 589            |
| 2026-01-02 | 810               | 610            |
| 2026-01-01 | 959               | 606            |
| 2025-12-31 | 782               | 598            |
| 2025-12-30 | 441               | 352            |

### Trend Observations

1. **Consistent daily volume**: ~500-800 flagged deliveries per full day
2. **New Year's spike**: Jan 1 had the highest count (959) - possibly holiday-related behavior
3. **7-day total**: ~4,230 flagged deliveries involving ~3,073 unique dashers

---

## Query: Total Count of Flagged Deliveries (3-day snapshot)

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
        AND COUNT(*) >= 5
);
```

### Results (Run: 2026-01-06, last 3 days)

| TOTAL_FLAGGED_DELIVERIES | UNIQUE_DASHERS |
|--------------------------|----------------|
| 1,034                    | 716            |

### Key Insight
- Average of ~1.44 flagged deliveries per dasher suggests most are isolated incidents
- However, there are clear repeat offenders (see below)

---

## Query: Repeat Offender Dashers

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
        AND COUNT(*) >= 5
) gps
GROUP BY gps.DASHER_ID
ORDER BY flagged_deliveries DESC
LIMIT 20;
```

### Results (Run: 2026-01-06, last 3 days)

| DASHER_ID | FLAGGED_DELIVERIES | TOTAL_PINGS |
|-----------|-------------------|-------------|
| 68143350  | 52                | 29,660      |
| 67938948  | 42                | 1,794       |
| 67924959  | 42                | 1,857       |
| 67951383  | 41                | 1,903       |
| 67938676  | 41                | 1,654       |
| 68038246  | 11                | 5,188       |
| 24248598  | 10                | 629         |
| 68017527  | 10                | 7,214       |
| 68172153  | 9                 | 4,579       |
| 66085724  | 8                 | 395         |
| 66711591  | 6                 | 291         |
| 58657740  | 5                 | 89          |
| 62810616  | 4                 | 202         |
| 36104573  | 4                 | 86          |
| 63627649  | 3                 | 18          |
| 64778456  | 3                 | 27          |
| 63855238  | 3                 | 34          |
| 46392044  | 3                 | 71          |
| 33459395  | 3                 | 172         |
| 1773715   | 3                 | 54          |

### Observations

1. **Top offender**: Dasher 68143350 has **52 flagged deliveries** with 29,660 total static pings in just 3 days - highly suspicious
2. **Cluster of similar behavior**: Dashers 67938948, 67951383, 67924959, 67938676 all have 41-42 flagged deliveries with similar ping counts (1,654-1,903)
   - Similar dasher IDs and behavior suggest these might be coordinated or using the same spoofing tool
3. **High ping counts**: Some dashers (68143350, 68017527, 68038246, 68172153) have very high ping counts, indicating prolonged periods of spoofed location

---

## Summary

| Metric | Value |
|--------|-------|
| Total flagged deliveries (3 days) | 1,034 |
| Unique dashers flagged | 716 |
| Top repeat offender | Dasher 68143350 (52 deliveries) |
| Dashers with 40+ flagged deliveries | 5 |
| Dashers with 10+ flagged deliveries | 8 |

---

## Next Steps
- Investigate the top 5 repeat offenders in detail
- Check if these deliveries had unusual completion patterns
- Analyze lat/lng variance for these same deliveries
- Look for device/app version patterns among repeat offenders

