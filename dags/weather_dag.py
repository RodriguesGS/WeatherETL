import pandas as pd
import sys
import os

from datetime import datetime, timedelta
from airflow.sdk import dag, task
from pathlib import Path

sys.path.insert(0, '/opt/airflow/src')

from extract import extract_data
from load_data import load_weather_data
from transform import data_transformations
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
load_dotenv(env_path)

API_KEY = os.getenv('API_KEY')

@dag(
    dag_id = 'weather_pipeline',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'retries': 2,
        'retry_delay': timedelta(minutes=5)
    },
    description='Pipeline ETL - Clima Maringá',
    schedule='@hourly',
    start_date=datetime(2026, 3, 10),
    catchup=False,
    tags=['weather', 'etl']
)

def weather_pipeline():
    
    @task
    def extract():
        
        url = f'https://api.openweathermap.org/data/2.5/weather?q=Maringá,BR&units=metric&appid={API_KEY}'
        
        extract_data(url)

    @task
    def transform():
        
        df = data_transformations()
        df.to_parquet('/opt/airflow/data/temp_data.parquet', index=False)
        
    @task
    def load():

        df = pd.read_parquet('/opt/airflow/data/temp_data.parquet')
        load_weather_data('mga_weather', df)
        
    extract()
    transform()
    load()
    
weather_pipeline()