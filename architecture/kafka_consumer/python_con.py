# Kafka Broker에 있는 데이터를 Consume 해서 Logstash가 listen 하고 있는 파일에 내용을 추가한다.

# Logstash가 listn 하고 있는 파일에 내용이 추가되면 Logstash가 반응해서 ElasticSearch에 적재할 것이다

# Library
from kafka import KafkaConsumer
import json
from pytz import timezone
import os
from threading import Semaphore
import time
from datetime import datetime

# 프로그램이 시작됐다는 것을 알린다.
start_time = time.time()


# Sempahore를 정의한다.
# Semaphore란 공유 영역에 어떤 프로세스나 스레드가 접근하는 것을 막기 위한 개념이다.
# 예를 들어 Sempahore의 수를 1로 지정하면 공유 영역에 들어가는 프로세스나 스레드는 1개여야 한다.
# 나머지 프로세스와 스레드는 기다려야 한다.
semaphore = Semaphore(1)

# Topic명을 정의한다.
kafka_topic = "kafka_topic"

# KafkaConsumer 객체를 정의한다.
consumer = KafkaConsumer(
    kafka_topic,

    # Kafka Broker 목록 정의
    bootstrap_servers=[
        "kafka_server1:9092,kafka_server2:9092,kafka_server3:9092"],

    group_id=None,

    consumer_timeout_ms=200000,  # 데이터가 없을 때 빠르게 종료하기 위한 설정(200초)

    # auto_offset_reset='latest', # earliest : 가장 초기 오프셋값, latest : 가장 마지막 오프셋값

    enable_auto_commit=False,  # 주기적으로 offset을 commit을 자동적으로 하지 않는다.
)

# 로그스태시가 실시간으로 감지할 파일 경로를 정의한다.
LOGSTASH_LISTEN_PATH = '/home/ubuntu/test/KimYeongu/Logstash_listen_file.log'

# 한강 관련 데이터 리스트
HANGANGS = [
    '강서한강공원',
    '광나루한강공원',
    '난지한강공원',
    '뚝섬한강공원',
    '망원한강공원',
    '반포한강공원',
    '양화한강공원',
    '여의도한강공원',
    '이촌한강공원',
    '잠실한강공원',
    '잠원한강공원',
]

# Kafka Broker에 적재된 데이터들을 for문으로 통해서 가져온다.
for i, message in enumerate(consumer):
    # 데이터를 utf-8로 디코딩한다.
    data = json.loads(message.value.decode('utf-8'))

    # filter 1. 한강 데이터인지 확인한다.
    if data['CITYDATA']['AREA_NM'] in HANGANGS:

        # filter 2. 6개의 속성을 추출하는 전처리해서 새로운 JSON 파일을 만든다.
        preprocessing_data = {
            # 도시 이름
            'AREA_NM':  data['CITYDATA']['AREA_NM'],

            # 현재 시간
            'DATE_TIME': datetime.now().strftime("%Y-%m-%d %H:%M"),

            # 인구 밀도

            # 인구 밀도 - 실시간 인구 지표 최솟값
            'AREA_PPLTN_MIN': int(data['CITYDATA']['LIVE_PPLTN_STTS'][0]['AREA_PPLTN_MIN']),

            # 인구 밀도 - 실시간 인구 지표 최댓값
            'AREA_PPLTN_MAX': int(data['CITYDATA']['LIVE_PPLTN_STTS'][0]['AREA_PPLTN_MAX']),

            # 인구 밀도 - 남성 인구 비율
            'MALE_PPLTN_RATE': float(data['CITYDATA']['LIVE_PPLTN_STTS'][0]['MALE_PPLTN_RATE']),

            # 인구 밀도 - 여성 인구 비율
            'FEMALE_PPLTN_RATE': float(data['CITYDATA']['LIVE_PPLTN_STTS'][0]['FEMALE_PPLTN_RATE']),

            # 인구 밀도 - 10대 실시간 인구 비율
            'PPLTN_RATE_10': float(data['CITYDATA']['LIVE_PPLTN_STTS'][0]['PPLTN_RATE_10']),

            # 인구 밀도- 20대 실시간 인구 비율
            'PPLTN_RATE_20': float(data['CITYDATA']['LIVE_PPLTN_STTS'][0]['PPLTN_RATE_20']),

            # 인구 밀도 - 30대 실시간 인구 비율
            'PPLTN_RATE_30': float(data['CITYDATA']['LIVE_PPLTN_STTS'][0]['PPLTN_RATE_30']),

            # 인구 밀도 속성 - 실시간 인구 데이터 업데이트 시간
            'LIVE_PPLTN_STTS': data['CITYDATA']['LIVE_PPLTN_STTS'][0]['PPLTN_TIME'],

            # 인구 밀도 속성 - 1 시간 후 예측 실시간 인구 지표 최솟값
            'FCST_PPLTN_MIN_1_HOUR_LATER': int(data['CITYDATA']['LIVE_PPLTN_STTS'][0]['FCST_PPLTN'][0]['FCST_PPLTN_MIN']),

            # 인구 밀도 속성 - 1 시간 후 예측 실시간 인구 지표 최댓값
            'FCST_PPLTN_MAX_1_HOUR_LATER': int(data['CITYDATA']['LIVE_PPLTN_STTS'][0]['FCST_PPLTN'][0]['FCST_PPLTN_MAX']),


            # 인구 밀도 속성 - 2 시간 후 예측 실시간 인구 지표 최솟값
            'FCST_PPLTN_MIN_2_HOUR_LATER': int(data['CITYDATA']['LIVE_PPLTN_STTS'][0]['FCST_PPLTN'][1]['FCST_PPLTN_MIN']),


            # 인구 밀도 속성 - 2 시간 후 예측 실시간 인구 지표 최댓값
            'FCST_PPLTN_MAX_2_HOUR_LATER': int(data['CITYDATA']['LIVE_PPLTN_STTS'][0]['FCST_PPLTN'][1]['FCST_PPLTN_MAX']),


            # 인구 밀도 속성 - 3 시간 후 예측 실시간 인구 지표 최솟값
            'FCST_PPLTN_MIN_3_HOUR_LATER': int(data['CITYDATA']['LIVE_PPLTN_STTS'][0]['FCST_PPLTN'][2]['FCST_PPLTN_MIN']),


            # 인구 밀도 속성 - 3 시간 후 예측 실시간 인구 지표 최댓값
            'FCST_PPLTN_MAX_3_HOUR_LATER': int(data['CITYDATA']['LIVE_PPLTN_STTS'][0]['FCST_PPLTN'][2]['FCST_PPLTN_MAX']),


            # 도로 혼잡도 속성 - 전체 도로 소통 평균 현황
            'ROAD_TRAFFIC_IDX': data['CITYDATA']['ROAD_TRAFFIC_STTS']['AVG_ROAD_DATA']['ROAD_TRAFFIC_IDX'],

            # 도로 혼잡도 속성 - 도로소통현황 업데이트 시간
            'ROAD_TRFFIC_TIME': data['CITYDATA']['ROAD_TRAFFIC_STTS']['AVG_ROAD_DATA']['ROAD_TRFFIC_TIME'],

            # 날씨 속성 - 날씨 데이터 업데이트 시간
            'WEATHER_TIME': data['CITYDATA']['WEATHER_STTS'][0]['WEATHER_TIME'],

            # 날씨 속성 - 체감 온도
            'WEATHER_STTS': float(data['CITYDATA']['WEATHER_STTS'][0]['SENSIBLE_TEMP']),

            # 날씨 속성 - 강수량
            'PRECIPITATION': 0 if data['CITYDATA']['WEATHER_STTS'][0]['PRECIPITATION'] == '-' else float(data['CITYDATA']['WEATHER_STTS'][0]['PRECIPITATION']),

            # 날씨 속성 - 강수 형태
            'PRECPT_TYPE': data['CITYDATA']['WEATHER_STTS'][0]['PRECPT_TYPE'],

            # 날씨 속성 - 강수 관련 메시지
            'PCP_MSG': data['CITYDATA']['WEATHER_STTS'][0]['PCP_MSG'],

            # 날씨 속성 - 초미세먼지
            'PM25': int(data['CITYDATA']['WEATHER_STTS'][0]['PM25']),

            # 날씨 속성 - 미세먼지
            'PM10': int(data['CITYDATA']['WEATHER_STTS'][0]['PM10']),

            # 날씨 속성 - 통합 대기 환경 등급
            'AIR_IDX': data['CITYDATA']['WEATHER_STTS'][0]['PM10'],

            # 날씨 속성 - 1 시간 후 강수 확률
            'RAIN_CHANCE_1_HOUR_LATER': int(data['CITYDATA']['WEATHER_STTS'][0]['FCST24HOURS'][0]['RAIN_CHANCE']),

            # 날씨 속성 - 2 시간 후 강수 확률
            'RAIN_CHANCE_2_HOUR_LATER': int(data['CITYDATA']['WEATHER_STTS'][0]['FCST24HOURS'][1]['RAIN_CHANCE']),

            # 날씨 속성 - 3 시간 후 강수 확률
            'RAIN_CHANCE_3_HOUR_LATER': int(data['CITYDATA']['WEATHER_STTS'][0]['FCST24HOURS'][2]['RAIN_CHANCE']),

        }

        # 공유 영역에 접근할 수 있는 프로세스 및 스레드를 1개로 지정하여
        # 다른 프로세스 및 스레드가 접근하지 못하도록 한다.
        with semaphore:
            with open(LOGSTASH_LISTEN_PATH, 'a') as f:
                # 파일의 내용을 쓴다.
                json.dump(preprocessing_data, f)

                # 이전 데이터와 현재 추가된 데이터와 구분을 하기 위해서 개행을 한다.
                f.write("\n")

                # kafka에 데이터를 넣어줌
                f.flush()

                # Logstash가 파일을 처리할 시간을 주기 위해 잠시 대기한다.
                time.sleep(3)


# Kafka Broker에 데이터가 있는지 확인했는데 특정 시간 이후 데이터가 없으면 아래 코드를 진행한다.


# LOGSTAH_LISTEN_PATH에 정의된 파일을 빈 내용 대치한다.
with open(LOGSTASH_LISTEN_PATH, 'w') as f:
    f.write('')

# 프로그램 실행 시간이 총 얼마나 걸리는지 확인한다.
end_time = time.time()
print(
    f"Kafka Consumer -> ElasticSearch execution time: {end_time - start_time:.2f} seconds")
print()
print()
