# postgresql 설정

- postgresql==16.3 설치
- 설정 변경1
  -  에어플로우의 postgresql의 port가 이미 5432 충돌로 port 변경
```
vi /etc/postgresql/16/main/opostgresql.conf

-----
port = 5433
listen_address = "0.0.0.0"

```


- 설정변경 2
  - 외부 접근 허용  
```
vi /etc/postgresql/16/main/pg_hba.conf

---
# 추가
host   all  all  0.0.0.0/0 scram-sha-256

```

# DB TABLE 스키마
```sql
CREATE TABLE Han_river_data (
    ID SERIAL PRIMARY KEY,
    AREA_NM VARCHAR(255) NOT NULL,
    AREA_PPLTN_MIN INT,
    AREA_PPLTN_MAX INT,
    MALE_PPLTN_RATE NUMERIC(5,2),
    FEMALE_PPLTN_RATE NUMERIC(5,2),
    PPLTN_RATE_10 NUMERIC(5,2),
    PPLTN_RATE_20 NUMERIC(5,2),
    PPLTN_RATE_30 NUMERIC(5,2),
    PPLTN_TIME TIMESTAMP,
    ROAD_TRAFFIC_IDX VARCHAR(255) ,
    ROAD_TRAFFIC_TIME TIMESTAMP,

    SENSIBLE_TEMP NUMERIC(5,2),
    PRECIPITATION INT,
    PRECPT_TYPE VARCHAR(255) ,
    PCP_MSG VARCHAR(255) ,
    PM25 INT,
    PM10 INT,
    AIR_IDX VARCHAR(255) ,
    WEATHER_TIME TIMESTAMP,

    FCST_PPLTN_MIN_1h INT,
    FCST_PPLTN_MAX_1h INT,
    FCST_PPLTN_MIN_2h INT,
    FCST_PPLTN_MAX_2h INT,
    FCST_PPLTN_MIN_3h INT,
    FCST_PPLTN_MAX_3h INT,

    RAIN_CHANCE_1h INT,
    RAIN_CHANCE_2h INT,
    RAIN_CHANCE_3h INT,

    TOTAL_CPCTY INT );
```
