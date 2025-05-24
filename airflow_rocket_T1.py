import requests
import json  
import airflow
import pendulum
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta  # 날짜/시간 처리를 위한 기본 라이브러리
from airflow import DAG  # Airflow의 핵심 DAG 클래스
import requests.exceptions
with DAG(
    dag_id="airflow_rocket_T1",
    schedule="0 0 * * *", #분,시,일,월,요일 언제 돌지 
    start_date=pendulum.datetime(2021, 1, 1, tz="Aisa/Seoul"), #dag이 언제부터 돌건지
    catchup=False, # 누락된 구간, 과거 날짜는 돌리지 않음 -> TRUE : 20210101 ~ 20250523 사이에 누락된 날짜가 모두 돌림
    dagrun_timeout=datetime.timedelta(minutes=60), #60분 이상 돌면 실패
    tags=["Table1"], 
   #params={"example_key": "example_value"},
) as dag:
    bash_t1 = BashOperator(
        task_id="bash_t1", #bash_id와 task_id 동일하게 
        bash_command="echo whoami",
    )
  bash_t2 = BashOperator(
        task_id="bash_t2", #bash_id와 task_id 동일하게 
        bash_command="echo $HOSTNAME",
    )
  bash_t1 >> bash_t2