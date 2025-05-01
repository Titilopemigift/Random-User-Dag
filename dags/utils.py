import requests
import pandas as pd
import json
import boto3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

secret_key = os.getenv("MY_SECRET_KEY")
access_key = os.getenv("MY_ACCESS_KEY")
region = os.getenv("REGION")

s3 = boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region
    )

# s3 Bucket details
s3_bucket = 'titilope-bucket'
s3_filename = 'random_users' 
s3_folder = 'random_users.json'

s3_path = f"s3://{s3_bucket}/{s3_folder}/{s3_filename}"

# Function to fetch data from the API and save it to a file
def random_users(**kwargs):
    
     """
    Fetches 10 random users from the random user generator API,
    normalizes the JSON structure into a DataFrame,
    and saves the result as a Parquet file in a temporary local directory.

    The local file path is then pushed to Airflow XCom for use in downstream tasks.

    Args:
        **kwargs: Context keyword arguments passed from Airflow.
                  Must include 'ti' (TaskInstance) for XCom operations.

    Returns:
        None
    """
     url = 'https://randomuser.me/api/?results=10'
     response = requests.get(url)
     data = response.json()
     users = data['results']
     df_users= pd.random_users(users)
     
     os.makedirs('random_users', exist_ok=True)
     file_path = 'random_users/random_users.parquet'
     df_users.to_parquet(file_path, engine='pyarrow', index=False)
     
     kwargs['ti'].xcom_push(key='local_file_path', value=file_path)

# Function to upload file to s3 bucket

def upload_to_s3(**kwargs):
     """
    Uploads a local Parquet file (created in a previous task) to an AWS S3 bucket.

    The local file path is retrieved from Airflow XCom.
    Uses boto3 to interact with the S3 service.

    Args:
        **kwargs: Context keyword arguments passed from Airflow.
                  Must include 'ti' (TaskInstance) to pull data from XCom.

    Returns:
        None
    """
     local_file_path = kwargs['ti'].xcom_pull(key='local_file_path')
     s3 = boto3.client('s3')
     s3.upload_file(local_file_path, s3_path)