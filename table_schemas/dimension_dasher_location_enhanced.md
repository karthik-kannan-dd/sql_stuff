# proddb.public.dimension_dasher_location_enhanced

Table containing dasher location data with GPS coordinates, device info, and delivery context.

## Schema

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| DASHER_ID | VARCHAR(16777216) | Y | Unique identifier for the dasher |
| LAT | FLOAT | Y | Latitude coordinate |
| LNG | FLOAT | Y | Longitude coordinate |
| SPEED | FLOAT | Y | Speed of the dasher |
| COURSE | FLOAT | Y | Direction/heading of travel |
| ALTITUDE | FLOAT | Y | Altitude reading |
| H_ACCURACY | FLOAT | Y | Horizontal accuracy of GPS reading |
| V_ACCURACY | FLOAT | Y | Vertical accuracy of GPS reading |
| TIME | TIMESTAMP_NTZ(9) | Y | Timestamp of the location reading |
| TIME_VARCHAR | VARCHAR(50) | Y | Timestamp as string |
| DEVICE_TYPE | VARCHAR(16777216) | Y | Type of device (iOS, Android, etc.) |
| MOTION_TYPE | VARCHAR(16777216) | Y | Type of motion (walking, driving, etc.) |
| MOTION_TYPE_CONFIDENCE | VARCHAR(16777216) | Y | Confidence level of motion type detection |
| VEHICLE_ID | VARCHAR(16777216) | Y | Vehicle identifier |
| VEHICLE_CATEGORY_ID | VARCHAR(16777216) | Y | Category of vehicle |
| SHIFT_ID | VARCHAR(16777216) | Y | Shift identifier for the dasher |
| CURRENT_STATUS | VARCHAR(16777216) | Y | Current dasher status |
| DELIVERY_UUID | VARCHAR(16777216) | Y | UUID of the active delivery |
| DEVICE_ID | VARCHAR(16777216) | Y | Device identifier |
| COUNTRY_ID | NUMBER(38,0) | Y | Country identifier |

## Example Queries

```sql
-- Get recent dasher locations for a specific delivery
SELECT
    DASHER_ID,
    LAT,
    LNG,
    SPEED,
    TIME,
    CURRENT_STATUS
FROM proddb.public.dimension_dasher_location_enhanced
WHERE DELIVERY_UUID = '<delivery_uuid>'
ORDER BY TIME DESC
LIMIT 100;
```

```sql
-- Analyze dasher movement patterns by motion type
SELECT
    MOTION_TYPE,
    COUNT(*) as location_count,
    AVG(SPEED) as avg_speed
FROM proddb.public.dimension_dasher_location_enhanced
WHERE TIME >= DATEADD(day, -1, CURRENT_TIMESTAMP())
GROUP BY MOTION_TYPE;
```
