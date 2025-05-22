#인터프리터 : airflow38로 변경
import requests
import json  
import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import requests.exceptions
from datetime import datetime, timedelta
dag =DAG(
  
  dag_id = "rocket_launches", #Dag Name
  start_date = datetime(2025,5,22,18,30), #2025년 5월 22일 18시 30분
  schedule = '@daily',
)
print("DAG")
print("DAG")
print("DAG")
print("DAG")
print("DAG")
print("DAG")
#깃 리포지토리 초기화 - 파일추가 - 커밋 - 원격 저장소 푸시 이거 하고 잔다 내가 

