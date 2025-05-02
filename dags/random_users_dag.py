from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from utils import etl_pipeline

default_args = {
    'owner': 'titilope'
    }

random_dag=DAG('random_user_to_s3',
         default_args=default_args,
         description="Fetch random users and upload to S3") 
    
random_users = PythonOperator(
        task_id='fetch_random_users',
        python_callable=etl_pipeline,
        dag = random_dag
    )

    

random_users
