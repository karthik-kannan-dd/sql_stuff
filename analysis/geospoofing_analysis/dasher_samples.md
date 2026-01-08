# Dasher Samples: High vs Low Delivery Counts

**Objective:** Compare behavior patterns between repeat offenders (many flagged deliveries) and single-instance dashers.

**Important:** All queries join with `DIMENSION_DELIVERIES` to ensure we only flag the dasher who actually completed the delivery (not dashers who were reassigned mid-delivery).

---

## High Delivery Count Dashers (Repeat Offenders)

### Dasher 68143350 - Top Offender (52 flagged deliveries)

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
  AND gps.DASHER_ID = '68143350'
  AND gps.DELIVERY_UUID IS NOT NULL
  AND dd.ACTIVE_DATE >= DATEADD(day, -3, CURRENT_DATE())
  AND dd.ACTUAL_DELIVERY_TIME IS NOT NULL
GROUP BY gps.DELIVERY_UUID, gps.DASHER_ID
HAVING MIN(gps.COURSE) = MAX(gps.COURSE) AND MIN(gps.ALTITUDE) = MAX(gps.ALTITUDE) AND COUNT(*) >= 5
ORDER BY first_ping
LIMIT 10;
```

| DELIVERY_UUID | PING_COUNT | COURSE | ALTITUDE | LAT | LNG | FIRST_PING | LAST_PING | DEVICE |
|---------------|------------|--------|----------|-----|-----|------------|-----------|--------|
| c1755138-7740-3001-86b5-bc1484eb111f | 800 | 0.0 | 2.0 | 42.7166 | -87.9533 | 2026-01-03 09:06:23 | 2026-01-03 09:22:14 | android |
| dc900a7a-33e4-3001-8649-324f7bc81d33 | 638 | 0.0 | 2.0 | 42.6971 | -87.8999 | 2026-01-03 09:22:39 | 2026-01-03 09:39:19 | android |
| 7a4a04f9-b88f-3001-9068-87cd6a6e3f57 | 179 | 0.0 | 2.0 | 42.7037 | -87.8316 | 2026-01-03 09:31:27 | 2026-01-03 09:34:59 | android |
| fe6d5dab-ccea-3001-a70b-a2818df895b9 | 564 | 0.0 | 2.0 | 42.6956 | -87.8905 | 2026-01-03 09:39:52 | 2026-01-03 09:50:56 | android |
| 3552208d-5a1f-3001-8578-93af9742122d | 599 | 0.0 | 2.0 | 42.6956 | -87.8905 | 2026-01-03 09:51:21 | 2026-01-03 10:03:11 | android |
| b80e754b-f841-3001-bc41-63730950902c | 556 | 0.0 | 2.0 | 42.5807 | -87.8537 | 2026-01-03 10:10:37 | 2026-01-03 10:21:35 | android |
| 9202717f-3c63-3001-802d-7e2e444e239c | 355 | 0.0 | 2.0 | 42.5814 | -87.5703 | 2026-01-03 10:21:47 | 2026-01-03 10:28:59 | android |
| 8a735404-90f4-3001-ba8e-9a1ad4c99946 | 195 | 0.0 | 2.0 | 42.5814 | -87.8568 | 2026-01-03 10:25:51 | 2026-01-03 10:32:41 | android |
| d758ef1f-4469-3001-b07a-b9422acddca8 | 833 | 0.0 | 2.0 | 42.8984 | -88.0103 | 2026-01-04 01:00:22 | 2026-01-04 01:17:02 | android |
| 30d28417-90a6-3001-a2b2-9785af29527c | 1033 | 0.0 | 2.0 | 42.8818 | -88.0591 | 2026-01-04 01:17:04 | 2026-01-04 01:37:41 | android |

**Observations:**
- **Device**: Android only
- **Location**: Wisconsin area (lat ~42.5-43.0, lng ~-87.5 to -88.0)
- **Pattern**: Consistent `course=0.0, altitude=2.0` - classic spoofing signature
- **Timing**: Back-to-back deliveries with minimal gaps (continuous spoofing)
- **Ping density**: Very high (179-1033 pings per delivery, ~10-20 min durations)

---

### Dasher 67938948 - Cluster Offender (42 flagged deliveries)

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
  AND gps.DASHER_ID = '67938948'
  AND gps.DELIVERY_UUID IS NOT NULL
  AND dd.ACTIVE_DATE >= DATEADD(day, -3, CURRENT_DATE())
  AND dd.ACTUAL_DELIVERY_TIME IS NOT NULL
GROUP BY gps.DELIVERY_UUID, gps.DASHER_ID
HAVING MIN(gps.COURSE) = MAX(gps.COURSE) AND MIN(gps.ALTITUDE) = MAX(gps.ALTITUDE) AND COUNT(*) >= 5
ORDER BY first_ping
LIMIT 10;
```

| DELIVERY_UUID | PING_COUNT | COURSE | ALTITUDE | LAT | LNG | FIRST_PING | LAST_PING | DEVICE |
|---------------|------------|--------|----------|-----|-----|------------|-----------|--------|
| 7b588631-f53b-3001-81d4-ff5b4db3e0d5 | 73 | 1.0 | 2.0 | 36.1395 | -85.6303 | 2026-01-04 04:03:02 | 2026-01-04 04:04:35 | android |
| 661f3f59-b46c-3001-8a19-e88cd4e53b98 | 42 | 1.0 | 2.0 | 36.1394 | -85.6302 | 2026-01-04 04:16:43 | 2026-01-04 04:17:36 | android |
| 25331b5e-9756-3001-bede-43b166877bd0 | 39 | 1.0 | 2.0 | 36.1394 | -85.6302 | 2026-01-04 04:17:59 | 2026-01-04 04:18:47 | android |
| 7f15d91c-539b-3001-aa85-636dbf9962dd | 43 | 1.0 | 2.0 | 36.1393 | -85.6301 | 2026-01-04 04:19:21 | 2026-01-04 04:20:13 | android |
| 07c3fc65-2ad5-3001-9082-4f749fdb5890 | 43 | 1.0 | 2.0 | 36.1393 | -85.6301 | 2026-01-04 04:20:47 | 2026-01-04 04:21:40 | android |
| 59f980a5-a933-3001-aada-0697957bb8ab | 30 | 1.0 | 2.0 | 36.1394 | -85.6302 | 2026-01-04 04:22:32 | 2026-01-04 04:23:08 | android |
| 4173f33f-b1c7-3001-af92-fc792f277464 | 36 | 1.0 | 2.0 | 36.1394 | -85.6302 | 2026-01-04 04:23:42 | 2026-01-04 04:24:24 | android |
| 35d9b7fc-468a-3001-b7a8-6a4f45e91f3c | 40 | 1.0 | 2.0 | 36.1395 | -85.6302 | 2026-01-04 04:25:04 | 2026-01-04 04:25:53 | android |
| b1870ad3-d1e4-3001-9999-d821e3b8844b | 41 | 1.0 | 2.0 | 36.1395 | -85.6302 | 2026-01-04 04:26:26 | 2026-01-04 04:27:15 | android |
| 3b977e1b-600d-3001-ad15-136a8508d97e | 77 | 1.0 | 2.0 | 36.1394 | -85.6302 | 2026-01-04 04:27:49 | 2026-01-04 04:29:26 | android |

**Observations:**
- **Device**: Android only
- **Location**: Tennessee area (lat ~36.14, lng ~-85.63) - SAME LOCATION for all deliveries!
- **Pattern**: `course=1.0, altitude=2.0` - slight variation from typical 0.0 signature
- **Timing**: Extremely rapid-fire deliveries (~1-2 min apart) - impossible without spoofing
- **Ping density**: Lower (30-77 pings), shorter delivery windows (~1 min each)
- **Red flag**: All deliveries from effectively the SAME GPS coordinates

---

## Low Delivery Count Dashers (Single Flagged Delivery)

```sql
SELECT
    gps.DELIVERY_UUID,
    gps.DASHER_ID,
    ping_count,
    course,
    altitude,
    lat,
    lng,
    first_ping,
    last_ping,
    device_type
FROM (
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
    HAVING MIN(gps.COURSE) = MAX(gps.COURSE) AND MIN(gps.ALTITUDE) = MAX(gps.ALTITUDE) AND COUNT(*) >= 5
) gps
WHERE gps.DASHER_ID IN (
    SELECT DASHER_ID FROM (
        SELECT
            gps2.DASHER_ID,
            COUNT(DISTINCT gps2.DELIVERY_UUID) as cnt
        FROM proddb.public.dimension_dasher_location_enhanced gps2
        INNER JOIN PRODDB.PUBLIC.DIMENSION_DELIVERIES dd2
            ON gps2.DELIVERY_UUID = dd2.DELIVERY_UUID
            AND gps2.DASHER_ID = dd2.DASHER_ID
        WHERE gps2.TIME >= DATEADD(day, -3, CURRENT_TIMESTAMP())
          AND gps2.DELIVERY_UUID IS NOT NULL
          AND dd2.ACTIVE_DATE >= DATEADD(day, -3, CURRENT_DATE())
          AND dd2.ACTUAL_DELIVERY_TIME IS NOT NULL
        GROUP BY gps2.DASHER_ID
        HAVING cnt = 1
    )
)
ORDER BY ping_count DESC
LIMIT 10;
```

| DELIVERY_UUID | DASHER_ID | PING_COUNT | COURSE | ALTITUDE | LAT | LNG | FIRST_PING | LAST_PING | DEVICE |
|---------------|-----------|------------|--------|----------|-----|-----|------------|-----------|--------|
| f8ce54e6-7aa3-3001-901b-89583af64f51 | 66388649 | 607 | 0.0 | 2.0 | 42.5614 | -87.8699 | 2026-01-03 06:50:08 | 2026-01-03 07:02:05 | android |
| c838367d-52ae-3001-9be6-2787470eeaea | 20521092 | 176 | -1.0 | 2.25 | 41.7417 | -74.0690 | 2026-01-04 12:08:08 | 2026-01-04 12:11:12 | ios |
| 96b4e961-e89c-3001-8df3-dcd664466b12 | 947304 | 57 | -1.0 | 119.68 | 40.0846 | -75.1653 | 2026-01-04 12:08:28 | 2026-01-04 12:11:11 | ios |
| 9dde0d1d-9271-3001-9b6f-cba2a1dffbd8 | 23725258 | 31 | 0.0 | 312.7 | 33.4765 | -112.0436 | 2026-01-04 12:10:16 | 2026-01-04 12:11:11 | android |

**Observations:**
- **Device mix**: Both iOS and Android (unlike repeat offenders who are Android-only)
- **Location variety**: Diverse locations across US
- **Altitude values**: More realistic/varied (2.25, 119.68, 312.7, etc.) vs artificial 2.0
- **Course values**: More varied (-1.0 for iOS, 0.0 for Android)
- **Exception**: Dasher 66388649 has the classic `course=0.0, altitude=2.0` pattern - likely actual spoofer

---

## Key Differences Summary

| Attribute | High Count (Repeat Offenders) | Low Count (Single Instance) |
|-----------|------------------------------|----------------------------|
| Device | Android only | Mix of iOS and Android |
| Course | 0.0 or 1.0 (artificial) | Varied (-1.0 iOS, 0.0 Android) |
| Altitude | 2.0 (artificial) | Varied realistic values |
| Location | Same area repeatedly | Diverse locations |
| Timing | Back-to-back rapid deliveries | Normal delivery intervals |
| Pattern | Consistent spoofing signature | May be GPS glitch or one-time event |

---

## Conclusion

**Repeat offenders** show clear signs of systematic GPS spoofing:
- Artificial default values (`course=0.0/1.0`, `altitude=2.0`)
- Same location for multiple deliveries
- Android devices (easier to spoof)
- Impossible delivery timing

**Single-instance dashers** are more likely to be:
- Legitimate GPS glitches
- Device malfunction
- One-time spoofing attempt (some still have suspicious patterns)

