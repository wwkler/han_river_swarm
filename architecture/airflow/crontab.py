# WORKFLOW
# 목표 : 서울시 실시간 도시 데이터를 API로 호출해서 받은 데이터를 전처리 한 후 Kafka Broker에 전송한다.
# API 설명 : 서울시 실시간 도시데이터는 실시간 인구현황, 도시소통현황, 주차장 현황, 지하철 실시간 도착 현황, 버스정류소 현황, 사고통제 현황, 따릉이 현황, 전기차 충전소 현황, 문화행사 현황을 종합적으로 제공한다.

# 데이터 수집은 다음과 같이 진행된다.
# 장소명을 이용해서 API를 호출하는 구조
# 장소는 115곳을 지원하므로 이에 115곳에 대한 장소에 대한 실시간 도시 데이터를 "동시"에 호출하고 받는다.
# results에는 115곳에 대한 실시간 도시 데이터가 있는데
# for문을 돌려서 1곳에 대한 실시간 도시 데이터를 받아서 Kafka Broker에 적재한다.

# Library
import aiohttp
import asyncio
import json
import time
from kafka import KafkaProducer

# 특정 도시의 실시간 도시 데이터를 가져오는 함수 (ex. 구로역의 실시간 도시 데이터를 가져온다. 동대문역의 실시간 도시 데이터를 가져온다.)


async def get_specific_city_data(session,
                                 area_nm,
                                 key,
                                 type_,
                                 start_index,
                                 end_index):
    # 호출할 API URL 설정
    url = f'http://openapi.seoul.go.kr:8088/{key}/{
        type_}/citydata/{start_index}/{end_index}/{area_nm}'

    # API URL를 호출한다.
    try:
        async with session.get(url) as response:
            # API URL를 호출하면서 상태 코드가 200인지 확인한다.
            if response.status == 200:
                # 반환된 데이터를 확인한다.
                json_ob = await response.json()

                # 데이터를 확인했는데 "정상 처리"된 데이터에 대한 로직 처리
                if json_ob['RESULT']['RESULT.CODE'] == 'INFO-000':
                    return area_nm, json_ob

                # 데이터를 확인했는데 "정상 처리"된 데이터가 아니면 데이터가 들어오지 않도록 한다.
                else:
                    return area_nm, None

            # API URL를 호출하면서 상태 코드가 200이 아니면 해당 도시에 대한 데이터는 누락 시킨다.
            else:
                return area_nm, None

    # API URL를 호출하는 과정에서 문제가 생기면 해당 도시에 대한 실시간 도시 데이터는 누락 시킨다.
    # 그래서 json_ob가 None으로 치환되서 return 된다.
    except aiohttp.ClientError as e:
        # print(f"Client error: {e}")
        return area_nm, None
    except json.JSONDecodeError as json_err:
        # print(f"JSON decode error: {json_err}")
        return area_nm, None
    except Exception as e:
        # print(f"An error occurred: {e}")
        return area_nm, None


# 서울시 실시간 도시 데이터를 비동기로 가져오는 메인 함수
async def get_seoul_realTime_data():
    # 프로그램이 시작됐다는 것을 알린다.
    start_time = time.time()

    # API를 호출하기 위한 세팅
    key = 'my_api'
    type_ = 'json'
    start_index = 1
    end_index = 1
    area_nm_list = [
        "강남 MICE 관광특구",
        "동대문 관광특구",
        "명동 관광특구",
        "이태원 관광특구",
        "잠실 관광특구",
        "종로·청계 관광특구",
        "홍대 관광특구",
        "경복궁",
        "광화문·덕수궁",
        "보신각",
        "서울 암사동 유적",
        "창덕궁·종묘",
        "가산디지털단지역",
        "강남역",
        "건대입구역",
        "고덕역",
        "고속터미널역",
        "교대역",
        "구로디지털단지역",
        "구로역",
        "군자역",
        "남구로역",
        "대림역",
        "동대문역",
        "뚝섬역",
        "미아사거리역",
        "발산역",
        "북한산우이역",
        "사당역",
        "삼각지역",
        "서울대입구역",
        "서울식물원·마곡나루역",
        "서울역",
        "선릉역",
        "성신여대입구역",
        "수유역",
        "신논현역·논현역",
        "신도림역",
        "신림역",
        "신촌·이대역",
        "양재역",
        "역삼역",
        "연신내역",
        "오목교역·목동운동장",
        "왕십리역",
        "용산역",
        "이태원역",
        "장지역",
        "장한평역",
        "천호역",
        "총신대입구(이수)역",
        "충정로역",
        "합정역",
        "혜화역",
        "홍대입구역(2호선)",
        "회기역",
        "4·19 카페거리",
        "가락시장",
        "가로수길",
        "광장(전통)시장",
        "김포공항",
        "낙산공원·이화마을",
        "노량진",
        "덕수궁길·정동길",
        "방배역 먹자골목",
        "북촌한옥마을",
        "서촌",
        "성수카페거리",
        "수유리 먹자골목",
        "쌍문동 맛집거리",
        "압구정로데오거리",
        "여의도",
        "연남동",
        "영등포 타임스퀘어",
        "외대앞",
        "용리단길",
        "이태원 앤틱가구거리",
        "인사동·익선동",
        "창동 신경제 중심지",
        "청담동 명품거리",
        "청량리 제기동 일대 전통시장",
        "해방촌·경리단길",
        "DDP(동대문디자인플라자)",
        "DMC(디지털미디어시티)",
        "강서한강공원",
        "고척돔",
        "광나루한강공원",
        "광화문광장",
        "국립중앙박물관·용산가족공원",
        "난지한강공원",
        "남산공원",
        "노들섬",
        "뚝섬한강공원",
        "망원한강공원",
        "반포한강공원",
        "북서울꿈의숲",
        "불광천",
        "서리풀공원·몽마르뜨공원",
        "서울광장",
        "서울대공원",
        "서울숲공원",
        "아차산",
        "양화한강공원",
        "어린이대공원",
        "여의도한강공원",
        "월드컵공원",
        "응봉산",
        "이촌한강공원",
        "잠실종합운동장",
        "잠실한강공원",
        "잠원한강공원",
        "청계산",
        "청와대",
        "북창동 먹자골목",
        "남대문시장"
    ]

    async with aiohttp.ClientSession() as session:
        # 특정 도시에 대해서 API를 비동기적으로 호출하고
        # 그에 대한 결과를 asyncio.gather를 이용해서 모은다.
        tasks = [get_specific_city_data(session,
                                        area_nm,
                                        key,
                                        type_,
                                        start_index,
                                        end_index)
                 for area_nm in area_nm_list]
        results = await asyncio.gather(*tasks)

        # results에는 115개의 실시간 도시 데이터가 있다.
        # for문을 돌리면 1개의 실시간 도시 데이터가 나오고
        # 그것을 바탕으로 Kafka Topic 명을 가지고 Kafka Produce 할 수 있도록 한다.
        for area_nm, json_ob in results:
            if json_ob is not None:
                print()
                print()
                print(f"------------- 성공 : {area_nm} -------------")
                print(f'{area_nm}에 대한 실시간 도시 데이터를 Kafka Produce 합니다...')
                print()
                print()

                # 실시간 도시데이터를 Kafka Producer 코드를 이용해 Kafka Broker에 적재하는 함수를 실행한다.
                make_kafka_producer(json_ob)

            else:
                print()
                print()
                print(f"------------- 실패 : {area_nm}  -------------")
                print(
                    f"{area_nm}에 대해서 실시간 도시 데이터를 수집하는 과정에서 문제가 생겨서 Kafka Produce 하지 못합니다...")
                print()
                print()

    # 프로그램 실행 시간이 총 얼마나 걸리는지 확인한다.
    end_time = time.time()
    print(f"API 데이터 수집 -> Kafka Broker 적재 완료까지 Total execution time: {
          end_time - start_time:.2f} seconds")
    print()
    print()

# 실시간 도시 데이터를 Kafka Producer 코드를 이용해 Kafka Broker에 적재하는 함수


def make_kafka_producer(json_ob):
    # kafka information
    broker1 = 'kafka_broker_server1_ip:9092'
    broker2 = 'kafka_broker_server2_ip:9092'
    broker3 = 'kafka_broker_server3_ip:9092'

    kafka_bootstrap_servers = [broker1, broker2, broker3]
    kafka_topic = 'kafka_topic'

    producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_servers)
    producer.send(kafka_topic,  value=json.dumps(json_ob).encode('utf-8'))
    producer.flush()


# 이벤트 루프를 실행하여 비동기 함수 호출
asyncio.run(get_seoul_realTime_data())
