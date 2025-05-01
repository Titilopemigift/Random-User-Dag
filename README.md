# Random User Data Pipeline with Airflow

This project is an Apache Airflow DAG that performs the following steps:

- Fetches 10 random users from the [Random User Generator API](https://randomuser.me/).

- Saves the data as a JSON file locally inside the Airflow environment.

- Uploads the JSON file to a specified AWS S3 bucket.


