import requests
import pandas as pd
import boto3
import awswrangler as wr
from airflow.models import Variable


# Function to fetch data from an API
def random_users():
    
     """
    Fetches random users from the random user generator API

    Returns:
        JSON file
    """
     url = 'https://randomuser.me/api/?results=10'
     response = requests.get(url, timeout=10)
     print("Data successfully extracted")
     return response.json()['results']

# Function normalize data
def normalize_data(data):

    """
    Transform and normalize data

    Returns:
        JSON file
    """
# Convert to dataframe
    df_result = pd.json_normalize(data)
    df_result = df_result.astype(str)
    print("Transformation successful")
    return df_result

# s3 Bucket details
s3_bucket = 'titilope-bucket'
s3_filename = 'random_users' 
s3_folder = 'random_users'

s3_path = f"s3://{s3_bucket}/{s3_folder}/{s3_filename}"

# boto3 session
session = boto3.Session(
        aws_access_key_id=Variable.get("MY_ACCESS_KEY"),
        aws_secret_access_key=Variable.get("MY_SECRET_KEY"),
        region_name = Variable.get("REGION_NAME")
    )
def load_data(df):
    """
Load dataframe as a parquet file to S3
    """
    wr.s3.to_parquet(
    df = df, 
    path=s3_path,
    dataset=True,
    mode='append',
    index=False,
    boto3_session=session)

print (f"Data successfully uploaded to {s3_path}")

# ETL pipeline

def etl_pipeline():
    extract = random_users()
    transform = normalize_data(extract)
    load_data(transform)


    print("ETL pipeline successful")


