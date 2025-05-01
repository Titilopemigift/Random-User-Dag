from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from utils import etl_pipeline

default_args = {
    'owner': 'titilope',
    'retries': 1,
    'retry_delay' : datetime.timedelta(seconds=2)
    }

with DAG(dag_id='random_user_to_s3',
         default_args=default_args,
         description="Fetch random users and upload to S3") as dag:
    
    random_users = PythonOperator(
        task_id='fetch_random_users',
        python_callable=etl_pipeline
    )

    

    random_users
