from pyspark import SparkContext
from pyspark.sql import SparkSession
import json
from datetime import datetime
from elasticsearch import Elasticsearch
import pytz

sc = SparkSession.builder.appName("kafka Example").getOrCreate()
sc.sparkContext.setLogLevel('ERROR')

df = sc.readStream.format("kafka").option("kafka.bootstrap.servers", "kafka_server1:9092,kafka_server2:9092,kafka_server3:9092").option(
    "subscribe", "kafka_topic").option("startingOffsets", "latest").load()

print(df.printSchema())

# 엘라스틱 서치 인덱스
index = "seoul_api_data_time_backup"


def process_batch(batch_df, batch_id):
    # 배치의 'value' 열을 처리하는 코드
    values = batch_df.select("value").rdd.flatMap(lambda row: row).collect()
    # 실시간으로 데이터를 출력하거나 다른 작업 수행
    # print(f"Batch ID: {batch_id}, Values: {type(values)}")

    # time zone 설정
    seoul_tz = pytz.timezone('Asia/Seoul')

    for value in values:
        value_dict = json.loads(value)
        if '한강' in value_dict['CITYDATA']['AREA_NM']:
            print(value_dict['CITYDATA']['AREA_NM'])

            # 파트 구분
            ppltn = value_dict['CITYDATA']['LIVE_PPLTN_STTS'][0]
            road = value_dict['CITYDATA']['ROAD_TRAFFIC_STTS']['AVG_ROAD_DATA']
            weather = value_dict['CITYDATA']['WEATHER_STTS'][0]

            # 강수량 전처리
            if weather['PRECIPITATION'] == "-":
                value_dict['CITYDATA']['WEATHER_STTS'][0]['PRECIPITATION'] = "0"

            preprocessing_data = {
                # 도시이름 추가
                'AREA_NM': value_dict['CITYDATA']['AREA_NM'],

                # 현재 시간
                'DATE_TIME': datetime.now().strftime('%Y-%m-%dT%H:%M'),

                # 인구 밀도 부분 전처리
                'AREA_PPLTN_MIN': int(ppltn['AREA_PPLTN_MIN']),
                'AREA_PPLTN_MAX': int(ppltn['AREA_PPLTN_MAX']),
                'MALE_PPLTN_RATE': float(ppltn['MALE_PPLTN_RATE']),
                'FEMALE_PPLTN_RATE': float(ppltn['FEMALE_PPLTN_RATE']),
                'PPLTN_RATE_10': float(ppltn['PPLTN_RATE_10']),
                'PPLTN_RATE_20': float(ppltn['PPLTN_RATE_20']),
                'PPLTN_RATE_30': float(ppltn['PPLTN_RATE_30']),
                'PPLTN_TIME': seoul_tz.localize(datetime.strptime(ppltn['PPLTN_TIME'], "%Y-%m-%d %H:%M")),
                'FCST_PPLTN_MIN_1h': int(ppltn['FCST_PPLTN'][0]['FCST_PPLTN_MIN']),
                'FCST_PPLTN_MIN_2h': int(ppltn['FCST_PPLTN'][1]['FCST_PPLTN_MIN']),
                'FCST_PPLTN_MIN_3h': int(ppltn['FCST_PPLTN'][2]['FCST_PPLTN_MIN']),
                'FCST_PPLTN_MAX_1h': int(ppltn['FCST_PPLTN'][0]['FCST_PPLTN_MAX']),
                'FCST_PPLTN_MAX_2h': int(ppltn['FCST_PPLTN'][1]['FCST_PPLTN_MAX']),
                'FCST_PPLTN_MAX_3h': int(ppltn['FCST_PPLTN'][2]['FCST_PPLTN_MAX']),

                # 도로 혼잡도 전처리
                'ROAD_TRAFFIC_IDX': road['ROAD_TRAFFIC_IDX'],
                'ROAD_TRFFIC_TIME': seoul_tz.localize(datetime.strptime(road['ROAD_TRFFIC_TIME'], "%Y-%m-%d %H:%M")),

                # 날씨 전처리
                'WEATHER_TIME': seoul_tz.localize(datetime.strptime(weather['WEATHER_TIME'], "%Y-%m-%d %H:%M")),
                'SENSIBLE_TEMP': float(weather['SENSIBLE_TEMP']),
                'PRECIPITATION': float(weather['PRECIPITATION']),
                'PRECPT_TYPE': weather['PRECPT_TYPE'],
                'PCP_MSG': weather['PCP_MSG'],
                'PM25': weather['PM25'],
                'PM10': weather['PM10'],
                'AIR_IDX': weather['AIR_IDX'],
                'RAIN_CHANCE_1h': weather['FCST24HOURS'][0]['RAIN_CHANCE'],
                'RAIN_CHANCE_2h': weather['FCST24HOURS'][1]['RAIN_CHANCE'],
                'RAIN_CHANCE_3h': weather['FCST24HOURS'][2]['RAIN_CHANCE'],
            }

            print(datetime.now())
            print(preprocessing_data['PPLTN_TIME'])
            # 엘라스틱 서치로 전처리한 데이터 넘겨주기
            es = Elasticsearch(["http://es_server_ip:9200"])
            es.index(index=index,  body=preprocessing_data)
            print(datetime.now())


query = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
    .writeStream\
    .foreachBatch(process_batch)\
    .outputMode("append")\
    .start()


query.awaitTermination()
