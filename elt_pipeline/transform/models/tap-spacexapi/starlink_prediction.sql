{{
  config(
    materialized='table'
  )
}}



WITH base AS (
    SELECT *
    FROM {{ source('tap-spacexapi', 'starlink') }}
), 

raw_starlink_data AS 
(SELECT
  DISTINCT  
  id,
  launch AS launch_id,
  CURRENT_TIMESTAMP AS transformation_updated_at,
  "spaceTrack" ->>'OBJECT_ID' AS satellite_id,
  "spaceTrack" ->>'OBJECT_NAME' AS satellite_name,
  "spaceTrack" ->>'OBJECT_TYPE' AS object_type,
  "spaceTrack" ->>'CREATION_DATE' AS creation_date,
  "spaceTrack" ->>'LAUNCH_DATE' AS launch_date,
  "spaceTrack" ->>'TIME_SYSTEM' AS time_system,
  "spaceTrack" ->>'COUNTRY_CODE' AS country_code,
  version
FROM base 
)

SELECT * FROM raw_starlink_data 
WHERE launch_date IS NOT NULL