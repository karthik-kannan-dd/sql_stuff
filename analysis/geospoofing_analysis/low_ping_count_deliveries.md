# Low Ping Count Deliveries Analysis

**Objective:** Identify deliveries with very few GPS pings (1-4) that still show static course/altitude - potentially suspicious as legitimate deliveries typically generate many pings.

**Rationale:** A delivery with only 1-4 pings but static course/altitude values could indicate:
- GPS spoofing app that crashed or was detected
- Brief spoofing attempt before switching methods
- Device/app issues causing GPS data loss
- Intentional minimal data to avoid detection

**Important:** All queries join with `DIMENSION_DELIVERIES` to ensure we only flag the dasher who actually completed the delivery (not dashers who were reassigned mid-delivery).

---

## Query: Deliveries with 1-4 Pings (Static Course/Altitude)

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
    TIMESTAMPDIFF(second, MIN(gps.TIME), MAX(gps.TIME)) as duration_seconds,
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
    AND COUNT(*) BETWEEN 1 AND 4
ORDER BY ping_count DESC, duration_seconds DESC
LIMIT 20;
```

### Results (Run: 2026-01-06, last 3 days)

| DELIVERY_UUID | DASHER_ID | PINGS | COURSE | ALTITUDE | LAT | LNG | DURATION | DEVICE |
|---------------|-----------|-------|--------|----------|-----|-----|----------|--------|
| 8fc1f0cc-8789-3001-9d9f-7354df3602ea | 13051422 | 4 | -1.0 | 16.8 | 37.73 | -122.39 | 39s | ios |
| 1da6bc20-ba5b-3001-b372-f0ed0a56a076 | 21316095 | 4 | 0.0 | 32.8 | -37.99 | 145.18 | 34s | android |
| ea2c7845-9151-3001-8aed-51d0a51fc10d | 48193429 | 4 | -1.0 | 13.8 | 25.87 | -80.17 | 20s | ios |
| 193bf5fe-4316-3001-ad47-6190d6df0aef | 20661080 | 4 | -1.0 | 201.7 | 35.17 | -80.85 | 20s | ios |
| 956f43e7-2b35-3001-93d5-7a819f85f3f1 | 26494273 | 4 | -1.0 | 13.6 | 45.45 | -73.49 | 19s | ios |
| d183cae2-53bd-3001-a2ab-e9450eff9bc0 | 46306383 | 4 | -1.0 | 182.6 | 41.86 | -87.64 | 19s | ios |
| eb271ac5-a942-3001-a1e6-e4785951ae3 | 29282718 | 4 | -1.0 | 6.1 | 40.73 | -74.05 | 19s | ios |
| cea34e25-741b-3001-98ed-d6e72b4b442f | 46306383 | 4 | -1.0 | 182.9 | 41.86 | -87.63 | 18s | ios |
| 8d4e036c-fb99-3001-a31f-01802497f66 | 16302622 | 4 | -1.0 | 252.8 | 44.98 | -93.26 | 18s | ios |
| 85e806ea-edd0-3001-945d-e5b3231139ae | 65144448 | 4 | -1.0 | 217.1 | 41.87 | -87.65 | 18s | ios |
| a9b6dc23-5291-3001-924e-858eb13e7e75 | 20692083 | 4 | -1.0 | 21.7 | 39.95 | -75.17 | 18s | ios |
| 61c0e511-63f6-3001-88b5-dbc35e51cf08 | 66463737 | 4 | -1.0 | 29.4 | 40.86 | -73.83 | 18s | ios |
| 97ad1953-0a9c-3001-b103-3acccee3cf1f | 63057183 | 4 | -1.0 | 56.0 | 40.84 | -73.94 | 18s | ios |
| 1d7ecb7e-54e6-3001-a2bb-4f9c293e1402 | 24147340 | 4 | -1.0 | 49.1 | 40.88 | -73.91 | 18s | ios |
| 30d4c87f-46ef-3001-9e76-aa7c15b1040a | 6400888 | 4 | 0.0 | 156.3 | 39.80 | -77.73 | 18s | android |
| 7b3207c0-f2f1-3001-84fa-7b33304f4bc2 | 8054712 | 4 | -1.0 | 219.1 | 41.99 | -88.30 | 18s | ios |
| 20a547bd-cc88-3001-a406-6f5c0ed2b9c3 | 66017235 | 4 | -1.0 | 16.4 | 40.75 | -73.94 | 18s | ios |
| f2f49db9-73f4-3001-96fe-29882db7587d | 52379003 | 4 | -1.0 | 14.6 | 40.72 | -73.98 | 18s | ios |
| 079dbda6-e6a3-3001-9c9d-5072f6ebb5d7 | 47301862 | 4 | -1.0 | 21.4 | 40.70 | -73.93 | 18s | ios |
| b97cc0eb-a7d5-3001-bb4f-766ff442bdcc | 55068810 | 4 | -1.0 | 34.0 | 40.78 | -73.73 | 18s | ios |

### Observations

1. **Shorter durations with completion filter**:
   - Maximum duration is now **39 seconds** (vs 8+ minutes before)
   - The longer-duration low-ping deliveries were likely from reassigned dashers
   - These short durations (~18-39 seconds) are more likely legitimate GPS initialization issues

2. **Device patterns**:
   - **iOS dominates**: 18 out of 20 are iOS devices with `course=-1.0`
   - Only 2 Android devices with `course=0.0`
   - This suggests low-ping patterns are more common on iOS (normal behavior vs spoofing)

3. **Course values**:
   - iOS: `course=-1.0` (iOS-specific placeholder/default when GPS not fully initialized)
   - Android: `course=0.0` (more suspicious but only 2 cases)

4. **Altitude values**:
   - Much more realistic values (6.1m to 252.8m) compared to artificial 2.0
   - One anomaly: lat=-37.99 (Australia) which is unusual given other US locations

5. **Key difference from high-ping analysis**:
   - Low-ping deliveries after completion filter are mostly iOS with short durations
   - This appears to be normal GPS behavior (brief initialization) rather than spoofing
   - Contrast with high-ping repeat offenders who are all Android with artificial values

---

## Key Indicators for Spoofing

| Indicator | Suspicious Value | Notes |
|-----------|-----------------|-------|
| Course | 0.0 | Android default/spoofing signature |
| Course | -1.0 | iOS placeholder value (often legitimate) |
| Altitude | 2.0 | Common spoofing default |
| Altitude | Negative | Impossible - below sea level |
| Pings/Duration | <1 ping/minute | GPS data being suppressed |

---

## Conclusion

After applying the completion filter, the low-ping deliveries show very different characteristics:
- Mostly iOS devices with short durations (18-39 seconds)
- Realistic altitude values
- Less suspicious overall - likely GPS initialization rather than spoofing
- The previous long-duration low-ping flags were from reassigned dashers, not spoofers

## Next Steps
- Cross-reference these dashers with high-ping flagged deliveries to find overlap
- Check if these dashers have other deliveries with normal GPS patterns
- Focus on high-ping repeat offenders as primary spoofing suspects
