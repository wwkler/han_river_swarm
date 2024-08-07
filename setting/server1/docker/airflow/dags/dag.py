from airflow import DAG
import pendulum
from airflow.operators.python import PythonOperator
from datetime import timedelta
from api_call import start
from kafka_api_producer import send_kafka_broker
from airflow.decorators import task
from datetime import datetime
# update
# 기본 args를 정의합니다.
default_args = {
    'owner': 'airflow',  # 여기에 소속 팀이나 사용자의 이름을 입력합니다.
    'depends_on_past': False,
    'retries': 5,  # 재시도 횟수를 5번으로 설정
    'retry_delay': timedelta(seconds=1),  # 재시도 간격을 1초로 설정
}

# DAG 정의
with DAG(
    dag_id = 'api_call_dag',
    default_args=default_args,
    start_date = pendulum.datetime(2023, 8, 6, tz = 'Asia/Seoul'),
    schedule = '*/5 * * * *',
    catchup = False,
) as dag:

    # API를 수집하는 Task
    @task(task_id = 'api_call')
    def api_call(**kwargs):
        start()

    # API 수집해서 모은 데이터들을 Kafka Broker에 적재하는 Task
    @task(task_id = 'api_producer')
    def api_producer(**kwargs):
        send_kafka_broker()

    api_call() >> api_producer()