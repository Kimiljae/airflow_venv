import requests
import json  
import airflow
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta  # 날짜/시간 처리를 위한 기본 라이브러리
from airflow import DAG  # Airflow의 핵심 DAG 클래스
from airflow.operators.python_operator import PythonOperator  # Python 함수를 실행하기 위한 Operator
from airflow.providers.mysql.hooks.mysql import MySqlHook  # MySQL 연결을 위한 Hook
import requests.exceptions
dag =DAG(
  dag_id = "rocket_launches", #Dag Name
  start_date = datetime(2025,5,22,18,30), #2025년 5월 22일 18시 30분
  schedule = '@daily',
)
download_launches = BashOperator ( #bashoperator를 이용해 curl로 URL 결과값 다운로드 
  task_id = "download_launches", # task 이름 
  bash_command="curl -o /tmp/launches.json -L 'https://ll.thespacedevs.com/2.0,0/launch/upcoming'", dag = dag 
)
#파이썬 함수는 결과값을 파싱하고 모든 로켓 사진을 다운로드
 def _get_pictures():
   #경로가 존재하는지 확인 
   pathlib.path("/tmp/images").mkdir(parents=True, exist_ok=True)
   #launches.json 파일에 있는 모든 그림 파일을 다운로드
   with open("/tmp/launches.json") as f :
     launches=json.load(f)
     image_urls = [launch["image"] for launch in launches["results"]]
     for image_url in image_urls:
       try: 
          response = requests.get(image_url)
          image_filename=image_url.split("/")[-1]
          target_file = f"/tmp/images/{image_filename}"
          with open(target_file,"wb") as f: 
            f.write(response.content)
            print(f"Downloaded {image_url} to {target_file}")
        except requests_exceptions.MissingSchema: 
          print(f"{image_url} appears to be an invalid URL.")
       except requests_exceptions.ConectionError: 
          print(f"Could not connect to {image_url}.")

_get_pictures = PythonOperator ( 
  task_id = "get_pictures",
  python_callable = _get_pictures,
  dag = dag,                               
)
notify = BashOperator ( 
  task_id = "notify",
  bash_command= 'echo "There are not $(ls/tmp/images/ | wc -l) images."',
  dag = dag                         
)

download_launches >> _get_pictures >> notify # 태스크 실행 순서 