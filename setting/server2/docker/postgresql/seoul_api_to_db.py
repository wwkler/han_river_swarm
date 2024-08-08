from kafka import KafkaConsumer
import json
from datetime import datetime
import psycopg2
import pytz

seoul_tz = pytz.timezone('Asia/Seoul')

# topic명을 정의한다.
kafka_topic = "seoul_api"
group_id = "seoul_api_sql"

target_city = ['POI085', 'POI087', 'POI090', 'POI093', 'POI094',
               'POI095', 'POI103', 'POI105', 'POI108', 'POI110', 'POI111']

# consumer 객체를 만든다.
consumer = KafkaConsumer(
    kafka_topic,

    bootstrap_servers=['kafka:29092']  # Kafka Cluster를 정의한다.

    , group_id=group_id,  # 이거 뭔지는 모르겠다.

    auto_offset_reset='latest',  # earliest : 가장 초기 오프셋값, latest : 가장 마지막 오프셋값

    enable_auto_commit=True,  # 주기적으로 offset을 auto commit하지 않겠다.
)


def preprocessing(data):
    # 파트 구분
    ppltn = data['CITYDATA']['LIVE_PPLTN_STTS'][0]

    road = data['CITYDATA']['ROAD_TRAFFIC_STTS'].get('AVG_ROAD_DATA')
    weather = data['CITYDATA']['WEATHER_STTS'][0]
    park = data['CITYDATA']['PRK_STTS']


    # 강수량 전처리
    if weather['PRECIPITATION'] == "-":
        data['CITYDATA']['WEATHER_STTS'][0]['PRECIPITATION'] = "0"



    preprocessing_data = {
        # 도시이름 추가
        'AREA_NM': data['CITYDATA']['AREA_NM'],

        # 인구 밀도 부분 전처리
        'AREA_PPLTN_MIN': int(ppltn['AREA_PPLTN_MIN']),
        'AREA_PPLTN_MAX': int(ppltn['AREA_PPLTN_MAX']),
        'MALE_PPLTN_RATE': float(ppltn['MALE_PPLTN_RATE']),
        'FEMALE_PPLTN_RATE': float(ppltn['FEMALE_PPLTN_RATE']),
        'PPLTN_RATE_10': float(ppltn['PPLTN_RATE_10']),
        'PPLTN_RATE_20': float(ppltn['PPLTN_RATE_20']),
        'PPLTN_RATE_30': float(ppltn['PPLTN_RATE_30']),
        'PPLTN_TIME': seoul_tz.localize(datetime.strptime(ppltn['PPLTN_TIME'], "%Y-%m-%d %H:%M")),


        # 날씨 전처리
        'SENSIBLE_TEMP': float(weather['SENSIBLE_TEMP']),
        'PRECIPITATION': float(weather['PRECIPITATION']),
        'PRECPT_TYPE': weather['PRECPT_TYPE'],
        'PCP_MSG': weather['PCP_MSG'],
        'PM25': weather['PM25'],
        'PM10': weather['PM10'],
        'AIR_IDX': weather['AIR_IDX'],
        'WEATHER_TIME': seoul_tz.localize(datetime.strptime(weather['WEATHER_TIME'], "%Y-%m-%d %H:%M")),

        'FCST_PPLTN_MIN_1h': int(ppltn['FCST_PPLTN'][0]['FCST_PPLTN_MIN']),
        'FCST_PPLTN_MAX_1h': int(ppltn['FCST_PPLTN'][0]['FCST_PPLTN_MAX']),
        'FCST_PPLTN_MIN_2h': int(ppltn['FCST_PPLTN'][1]['FCST_PPLTN_MIN']),
        'FCST_PPLTN_MAX_2h': int(ppltn['FCST_PPLTN'][1]['FCST_PPLTN_MAX']),
        'FCST_PPLTN_MIN_3h': int(ppltn['FCST_PPLTN'][2]['FCST_PPLTN_MIN']),
        'FCST_PPLTN_MAX_3h': int(ppltn['FCST_PPLTN'][2]['FCST_PPLTN_MAX']),

        'RAIN_CHANCE_1h': weather['FCST24HOURS'][0]['RAIN_CHANCE'],
        'RAIN_CHANCE_2h': weather['FCST24HOURS'][1]['RAIN_CHANCE'],
        'RAIN_CHANCE_3h': weather['FCST24HOURS'][2]['RAIN_CHANCE'],

    }
    # 도로 혼잡도 전처리
    if road:
        preprocessing_data['ROAD_TRAFFIC_IDX'] = road['ROAD_TRAFFIC_IDX']
        preprocessing_data['ROAD_TRAFFIC_TIME'] = seoul_tz.localize(datetime.strptime(road['ROAD_TRFFIC_TIME'], "%Y-%m-%d %H:%M"))

    else:
        preprocessing_data['ROAD_TRAFFIC_IDX'] = None
        preprocessing_data['ROAD_TRAFFIC_TIME'] = None

    sum_cpcty = 0
    for i in park:
        sum_cpcty += int(i['CPCTY'])

    preprocessing_data['TOTAL_CPCTY'] = sum_cpcty

    return preprocessing_data


def insert_into(data):
#    host = 'host.docker.internal'
    host = '172.31.9.214'
    port = 5433
    user = 'postgres'
    pw = 'postgres'
    db = 'seoul_api_db'
    table = 'han_river_data'
    conn = psycopg2.connect(host=host, port=port,
                            dbname=db, user=user, password=pw)
    cur = conn.cursor()

    sqlquery = '''
        INSERT INTO han_river_data (
            AREA_NM,
            AREA_PPLTN_MIN,
            AREA_PPLTN_MAX,
            MALE_PPLTN_RATE,
            FEMALE_PPLTN_RATE,
            PPLTN_RATE_10,
            PPLTN_RATE_20,
            PPLTN_RATE_30,
            PPLTN_TIME,
            ROAD_TRAFFIC_IDX,
            ROAD_TRAFFIC_TIME,
            SENSIBLE_TEMP,
            PRECIPITATION,
            PRECPT_TYPE,
            PCP_MSG,
            PM25,
            PM10,
            AIR_IDX,
            WEATHER_TIME,
            FCST_PPLTN_MIN_1h,
            FCST_PPLTN_MAX_1h,
            FCST_PPLTN_MIN_2h,
            FCST_PPLTN_MAX_2h,
            FCST_PPLTN_MIN_3h,
            FCST_PPLTN_MAX_3h,
            RAIN_CHANCE_1h,
            RAIN_CHANCE_2h,
            RAIN_CHANCE_3h,
            TOTAL_CPCTY
        ) VALUES (
            %(AREA_NM)s,
            %(AREA_PPLTN_MIN)s,
            %(AREA_PPLTN_MAX)s,
            %(MALE_PPLTN_RATE)s,
            %(FEMALE_PPLTN_RATE)s,
            %(PPLTN_RATE_10)s,
            %(PPLTN_RATE_20)s,
            %(PPLTN_RATE_30)s,
            %(PPLTN_TIME)s,
            %(ROAD_TRAFFIC_IDX)s,
            %(ROAD_TRAFFIC_TIME)s,
            %(SENSIBLE_TEMP)s,
            %(PRECIPITATION)s,
            %(PRECPT_TYPE)s,
            %(PCP_MSG)s,
            %(PM25)s,
            %(PM10)s,
            %(AIR_IDX)s,
            %(WEATHER_TIME)s,
            %(FCST_PPLTN_MIN_1h)s,
            %(FCST_PPLTN_MAX_1h)s,
            %(FCST_PPLTN_MIN_2h)s,
            %(FCST_PPLTN_MAX_2h)s,
            %(FCST_PPLTN_MIN_3h)s,
            %(FCST_PPLTN_MAX_3h)s,
            %(RAIN_CHANCE_1h)s,
            %(RAIN_CHANCE_2h)s,
            %(RAIN_CHANCE_3h)s,
            %(TOTAL_CPCTY)s
            );
    '''
    cur.execute(sqlquery, data)

    conn.commit()

    cur.close()
    conn.close()
    print("^^b")


for i, message in enumerate(consumer):
    try:
        data = json.loads(message.value.decode('utf-8'))
        if data['CITYDATA']['AREA_CD'] in target_city:
            pro_data = preprocessing(data)
            insert_into(pro_data)
    except Exception as error:
        print(error)
        continue
    except psycopg2.Error as error:
        print(error)
        continue
