import requests
import pandas as pd
import boto3
import os
import awswrangler as wr
from airflow.models import variable


# s3 Bucket details
s3_bucket = 'titilope-bucket'
s3_filename = 'random_users' 
s3_folder = 'random_users.json'

s3_path = f"s3://{s3_bucket}/{s3_folder}/{s3_filename}"

# Function to fetch data from the API
def random_users():
    
     """
    Fetches random users from the random user generator API

    Returns:
        JSON file
    """
     url = 'https://randomuser.me/api/?results=10'
     response = requests.get(url)
     print("Data successfully extracted")
     return response.json()['results']

# Function normalize data
def normalize_data(data):
   
# Convert to dataframe
   df_result = pd.json_normalize(data)
   df_result.columns = df_result.columns.astype(str)
   print("Transformation successful")
   return df_result


# boto3 session
session = boto3.Session(
        aws_access_key_id=variable.get("MY_SECRET_KEY"),
        aws_secret_access_key=variable.get("MY_ACCESS_KEY"),
        region = variable.get("REGION")
    )
def load_data():
# Function to upload dataframe as a parquet file to S3
    wr.s3.to_parquet(
    df = normalize_data, 
    path=s3_path,
    dataset=True,
    mode='append',
    index=False,
    boto3_session=session)

print (f"Data successfully uploaded to {s3_path}")

# ETL pipeline

def etl_pipeline():
    extract = random_users,
    transform = normalize_data(),
    load =load_data()
    print("data successfully")


