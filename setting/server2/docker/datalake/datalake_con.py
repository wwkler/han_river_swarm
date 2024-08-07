# Library
from kafka import KafkaConsumer
import json
import datetime
from pytz import timezone
import os
import time

# topic명을 정의한다.
kafka_topic = "seoul_api"
group_id = "datalake"

time.sleep(10)

# consumer 객체를 만든다.
consumer = KafkaConsumer(
    kafka_topic,

    bootstrap_servers=['kafka:29092'] # Kafka Cluster를 정의한다.

    ,group_id=group_id,

    auto_offset_reset='latest', # earliest : 가장 초기 오프셋값, latest : 가장 마지막 오프셋값

    enable_auto_commit=True,  # 주기적으로 offset을 auto commit하지 않겠다.
)

for i, message in enumerate(consumer):
    date = datetime.datetime.now(timezone('Asia/Seoul')).strftime("%Y%m%d_%H%M")
    try:
        data = json.loads(message.value.decode('utf-8'))
    except:
        print(message.value)
        continue
    #data 가 제대로 잘 들어왔는지 확인하는 코드
    try:
        date = data['CITYDATA']['ROAD_TRAFFIC_STTS']['AVG_ROAD_DATA']['ROAD_TRFFIC_TIME']
        date = date.replace(' ', "_")
        date = date.replace('-', "")
        date = date.replace(":", "")
    except:
        print(date, data)
        continue

    dir_path = f"/home/datalake/{date}"
    os.makedirs(dir_path, exist_ok = True)
    file_path = dir_path + "/{}.json"

    area = data['CITYDATA']['AREA_CD']
    with open(file_path.format( area), 'w', encoding="UTF-8") as f:
        json.dump(data, f)
        print(file_path.format(area))

print(f"{date} 완료 " )