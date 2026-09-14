from datetime import datetime, timedelta

from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.sensors.external_task import ExternalTaskSensor
from airflow.sdk import DAG
from common.ingestion import load_csv

default_args = {
    "owner": "data-engineering",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="ingestion_transaction",
    start_date=datetime(2026, 1, 1),
    schedule="0 2 * * *",
    catchup=False,
    default_args=default_args,
    tags=["ingestion"],
) as dag:

    wait_for_master = ExternalTaskSensor(
        task_id="wait_for_master",
        external_dag_id="ingestion_master",
        external_task_ids=[
            "load_customers",
            "load_products",
            "load_marketing_campaigns",
        ],
        allowed_states=["success"],
        failed_states=["failed", "upstream_failed"],
        execution_delta=timedelta(hours=1),
        poke_interval=30,
        timeout=60 * 30,
        mode="reschedule",
    )

    load_transactions = PythonOperator(
        task_id="load_transactions",
        python_callable=load_csv,
        op_kwargs={
            "table_name": "transactions",
            "file_name": "transactions.csv",
            "columns": [
                "transaction_id",
                "customer_id",
                "transaction_date",
                "total_amount",
            ],
            "required_columns": [
                "transaction_id",
                "customer_id",
                "transaction_date",
                "total_amount",
            ],
        },
    )

    wait_for_master >> load_transactions