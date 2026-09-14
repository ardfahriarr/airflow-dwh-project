from datetime import datetime, timedelta

from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import DAG
from common.ingestion import load_csv

default_args = {
    "owner": "data-engineering",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}


with DAG(
    dag_id="ingestion_master",
    start_date=datetime(2026, 1, 1),
    schedule="0 1 * * *",
    catchup=False,
    default_args=default_args,
    tags=["ingestion"],
) as dag:

    load_customers = PythonOperator(
        task_id="load_customers",
        python_callable=load_csv,
        op_kwargs={
            "table_name": "customers",
            "file_name": "customers.csv",
            "columns": [
                "customer_id",
                "name",
                "email",
                "city",
                "signup_date",
            ],
            "required_columns": [
                "customer_id",
                "name",
                "signup_date",
            ],
        },
    )

    load_products = PythonOperator(
        task_id="load_products",
        python_callable=load_csv,
        op_kwargs={
            "table_name": "products",
            "file_name": "products.csv",
            "columns": [
                "product_id",
                "product_name",
                "category",
                "price",
            ],
            "required_columns": [
                "product_id",
                "product_name",
                "price",
            ],
        },
    )

    load_campaigns = PythonOperator(
        task_id="load_marketing_campaigns",
        python_callable=load_csv,
        op_kwargs={
            "table_name": "marketing_campaigns",
            "file_name": "marketing_campaigns.csv",
            "columns": [
                "campaign_id",
                "campaign_name",
                "start_date",
                "end_date",
                "channel",
            ],
            "required_columns": [
                "campaign_id",
                "campaign_name",
                "start_date",
                "end_date",
            ],
        },
    )