from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd
from sqlalchemy import create_engine

# Konfigurasi Database
DB_CONN = "postgresql://admin_pipeline:DataEngineer2027!@localhost:5434/ipbd_wired"

def extract_from_api():
    response = requests.get("http://localhost:8000/articles")
    data = response.json()
    return data['articles']

def transform_and_load(**kwargs):
    ti = kwargs['ti']
    articles = ti.xcom_pull(task_ids='extract_data')
    
    df = pd.DataFrame(articles)
    
    # Transformasi sederhana
    df['scraped_at'] = pd.to_datetime(df['scraped_at'])
    
    # Simpan ke Database
    engine = create_engine(DB_CONN)
    df.to_sql('wired_articles', engine, if_exists='append', index=False)

default_args = {
    'owner': 'Trisha',
    'start_date': datetime(2026, 4, 21),
    'retries': 1,
}

with DAG('wired_extraction_pipeline', default_args=default_args, schedule_interval='@daily') as dag:
    
    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_from_api
    )
    
    load_task = PythonOperator(
        task_id='transform_and_load_data',
        python_callable=transform_and_load
    )

    extract_task >> load_task