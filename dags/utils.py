import requests
import json
import boto3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

secret_key = os.getenv("MY_SECRET_KEY")
access_key = os.getenv("MY_ACCESS_KEY")
region_key = os.getenv("REGION_KEY")

s3 = boto3.client(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        aws_region_key=region_key
    )

# s3 Bucket details
s3_bucket = 'titilope-bucket'
s3_filename = 'random_users' 
s3_folder = 'random_users.json'

s3_path = f"s3://{s3_bucket}/{s3_folder}/{s3_filename}"

# Function to fetch data from the API and save it to a file
def random_users(**kwargs):
    url = 'https://randomuser.me/api/?results=10'
    response = requests.get(url)
    data = response.json()

    os.makedirs('random_users', exist_ok=True)
    file_path = 'random_users/randome_users.json'
    with open(file_path, 'w') as f:
        json.dump(data, f)

    kwargs['ti'].xcom_push(key='local_file_path', value=file_path)

# Function to upload file to s3 bucket

def upload_to_s3(**kwargs):
    local_file_path = kwargs['ti'].xcom_pull(key='local_file_path')
    s3 = boto3.client('s3')
    s3.upload_file(local_file_path, s3_path)