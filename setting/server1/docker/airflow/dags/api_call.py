# Library
import aiohttp
import asyncio
import json
import time
from airflow.exceptions import AirflowException

# 특정 도시의 실시간 도시 데이터를 가져오는 함수 (ex. 구로역의 실시간 도시 데이터를 가져온다. 동대문역의 실시간 도시 데이터를 가져온 다.)


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

                # 데이터를 확인했는데 "정상 처리"된 데이터가 아니면 task를 다시 수행한다.
                else:
                    raise AirflowException("Task failed, will retry1111")

            # API URL를 호출하면서 상태 코드가 200이 아니면 task를 다시 수행한다.
            else:
                raise AirflowException("Task failed, will retry2222222")

    # API URL를 호출하는 과정에서 문제가 생기면 해당 도시에 대한 실시간 도시 데이터는 누락 시킨다.
    # 그래서 json_ob가 None으로 치환되서 return 된다.
    except aiohttp.ClientError as e:
        raise AirflowException("Task failed, will retry33333333")
    except json.JSONDecodeError as json_err:
        raise AirflowException("Task failed, will retry44444444")
    except Exception as e:
        raise AirflowException("Task failed, will retry5555555")

# 서울시 실시간 도시 데이터를 비동기로 가져오는 메인 함수


async def get_seoul_realTime_data():
    # API를 호출하기 위한 세팅
    key = 'your_api_key'
    type_ = 'json'
    start_index = 1
    end_index = 1
    area_nm_list = [
        'POI001', 'POI002', 'POI003', 'POI004', 'POI005', 'POI006', 'POI007', 'POI008', 'POI009', 'POI010',
        'POI011', 'POI012', 'POI013', 'POI014', 'POI015', 'POI016', 'POI017', 'POI018', 'POI019', 'POI020',
        'POI021', 'POI022', 'POI023', 'POI024', 'POI025', 'POI026', 'POI027', 'POI028', 'POI029', 'POI030',
        'POI031', 'POI032', 'POI033', 'POI034', 'POI035', 'POI036', 'POI037', 'POI038', 'POI039', 'POI040',
        'POI041', 'POI042', 'POI043', 'POI044', 'POI045', 'POI046', 'POI047', 'POI048', 'POI049', 'POI050',
        'POI051', 'POI052', 'POI053', 'POI054', 'POI055', 'POI056', 'POI057', 'POI058', 'POI059', 'POI060',
        'POI061', 'POI062', 'POI063', 'POI064', 'POI065', 'POI066', 'POI067', 'POI068', 'POI069', 'POI070',
        'POI071', 'POI072', 'POI073', 'POI074', 'POI075', 'POI076', 'POI077', 'POI078', 'POI079', 'POI080',
        'POI081', 'POI082', 'POI083', 'POI084', 'POI085', 'POI086', 'POI087', 'POI088', 'POI089', 'POI090',
        'POI091', 'POI092', 'POI093', 'POI094', 'POI095', 'POI096', 'POI097', 'POI098', 'POI099', 'POI100',
        'POI101', 'POI102', 'POI103', 'POI104', 'POI105', 'POI106', 'POI107', 'POI108', 'POI109', 'POI110',
        'POI111', 'POI112', 'POI113', 'POI114', 'POI115'
    ]

    # 115개에 대한 실시간 도시 데이터를 리스트에 저장하는 변수
    json_ob_all = []

    async with aiohttp.ClientSession() as session:
        # 특정 도시에 대해서 API를 비동기적으로 호출하고
        # 그에 대한 결과를 asyncio.gather를 이용해서 모아서 results에 저장한다.
        tasks = [get_specific_city_data(session,
                                        area_nm,
                                        key,
                                        type_,
                                        start_index,
                                        end_index)
                 for area_nm in area_nm_list]
        results = await asyncio.gather(*tasks)

        # for문으로 돌려서 특정 도시에 대한 실시간 도시 데이터를 가져온다.
        for area_nm, json_ob in results:
            if json_ob is not None:
                # 실시간 도시 데이터가 있으면 json_ob_all에 append 한다.
                # print(f"------------- 성공 : {area_nm} -------------")

                # 1개의 실시간 도시 데이터를 받아서 json_ob_all에 append한다.
                json_ob_all.append(json_ob)

            else:
                # 실시간 도시 데이터가 누락 되었으면 json_ob_all에 append 하지 못한다.
                print(f"------------- 실패 : {area_nm}  -------------")
                print(
                    f"{area_nm}에 대해서 실시간 도시 데이터를 수집하는 과정에서 문제가 생겨서 리스트에 추가하지 못했습니다...")

    # 리스트로 묶은 실시간 도시 데이터들을 파일 시스템에 저장하는 함수를 호출한다.
    store_file_system(json_ob_all)

# 리스트로 묶은 실시간 도시 데이터들을 파일 시스템에 저장한다.


def store_file_system(json_ob_all):
    # 데이터를 저장할 파일 경로
    FILE_PATH = '/opt/airflow/temp/list_realtime_city_data.json'

    with open(FILE_PATH, 'w') as f:
        json.dump(json_ob_all, f)


# 프로그램을 시작하는 함수
def start():
    # 프로그램이 시작됐다는 것을 알린다.
    #    start_time = time.time()

    # 이벤트 루프를 실행하여 비동기 함수 호출
    asyncio.run(get_seoul_realTime_data())

    # 프로그램 실행 시간이 총 얼마나 걸리는지 확인한다.
 #   end_time = time.time()
