# Library
from kafka import KafkaProducer
import time
import os
import json
from datetime import datetime

# 리스트로 묶여진 실시간 도시 데이터들을 파일 시스템에서 읽어서 Kafka Broker에 적재하는 함수
def send_kafka_broker():
    # 프로그램이 시작됐다는 것을 알린다.
    start_time = time.time()

    # kafka information
    kafka_bootstrap_servers = "kafka:29092"
    kafka_topic = "seoul_api"


    producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_servers)


    # 115개 실시간 도시 데이터들을 담은  데이터가 위치된 경로
    FILE_PATH = '/opt/airflow/temp/list_realtime_city_data.json'

    # FILE_PATH를 참고해서115개 실시간 도시 데이터들을 읽는다.
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r') as f:
            json_ob_all = json.load(f)

        # 리스트로 묶여진 실시간 도시 데이터들을 for문으로 돌려서 하나의 실시간 도시 데이터들을 받는다.
        # 그리그 그것을 kafka Produce 하여 Kafka Broker에 적재한다.
        for json_ob in json_ob_all:
            producer.send(kafka_topic, value=json.dumps(json_ob).encode('utf-8'))
        producer.flush()

        print(f'리스트에 들어 있는 실시간 도시 데이터 개수 : {len(json_ob_all)}')


    else:
        print("Data file not found.")

    # 프로그램 실행 시간이 총 얼마나 걸리는지 확인한다.
    end_time = time.time()
    print(f"Kafka Produce Total execution time: {end_time - start_time:.2f} seconds")
