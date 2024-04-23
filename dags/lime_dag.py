import pandas as pd 

import requests

import json
import logging
import os
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.hooks.S3_hook import S3Hook
from airflow.models import Variable

# The dag runs hourly automatically - the app also has an hourly live update

def _fetch_bikes_data(ti):
    """
    Fetch bike data : download bike data from opendata using api call - save json file into AWS
    """
    url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records?"
    try: 
        response = requests.get(url)
        response.raise_for_status()
        bikes = response.json()
        now = datetime.now().timestamp()
        json_bikes_filename = f"./data/bikes_{now}.json"
        pd.json_normalize(bikes["results"]).to_json(f"{json_bikes_filename}")
        logging.info(f"Bikes data dumped into {json_bikes_filename}")
        ti.xcom_push(key="json_bikes_filename", value=json_bikes_filename)
        s3_hook = S3Hook(aws_conn_id="aws_connection")
        s3_hook.load_file(
            filename=json_bikes_filename,
            key='bikes_data.json',
            bucket_name=Variable.get("S3BucketName"),
            replace=True
            )
    except Exception as e: 
        logging.info(e)    
    



def _transform_bikes_data(ti):
    """
    Transfroms json into csv and load it to S3 for the app to use
    """
    json_bikes_file  =ti.xcom_pull(key="json_bikes_filename")
    bikes = pd.read_json(json_bikes_file)
    csv_bikes_file = './data/bikes.csv'
    bikes.to_csv(csv_bikes_file, index=False)
    s3_hook = S3Hook(aws_conn_id="aws_connection")
    s3_hook.load_file(
        filename=csv_bikes_file,
        key="bikes_data.csv",
        bucket_name=Variable.get("S3BucketName"),
        replace=True
    )
    logging.info(f"Bikes data dumped into {csv_bikes_file}")


with DAG("lime_dag", start_date=datetime(2024, 1, 1), schedule_interval="@hourly", catchup=False) as dag:
    start = BashOperator(task_id="start", bash_command="echo 'Start!'")
    fetch_bikes_data = PythonOperator(task_id="fetch_bikes_data", python_callable=_fetch_bikes_data)
    transform_bikes_data = PythonOperator(task_id="transform_bikes_data", python_callable=_transform_bikes_data)
    end = BashOperator(task_id="end", bash_command="echo 'End!'")

    start >> fetch_bikes_data >> transform_bikes_data >> end 
