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
    dag_id="ingestion_transaction_item",
    start_date=datetime(2026, 1, 1),
    schedule="0 3 * * *",
    catchup=False,
    default_args=default_args,
    tags=["ingestion"],
) as dag:

    wait_for_transaction = ExternalTaskSensor(
        task_id="wait_for_transaction",
        external_dag_id="ingestion_transaction",
        external_task_ids=[
            "load_transactions"
        ],
        allowed_states=["success"],
        failed_states=["failed","upstream_failed"],
        execution_delta=timedelta(hours=1),
        poke_interval=30,
        timeout=60 * 30,
        mode="reschedule",
    )

    load_transaction_items = PythonOperator(
        task_id="load_transaction_items",
        python_callable=load_csv,
        op_kwargs={
            "table_name": "transaction_items",
            "file_name": "transaction_items.csv",
            "columns": [
                "transaction_item_id",
                "transaction_id",
                "product_id",
                "quantity",
                "price",
            ],
            "required_columns": [
                "transaction_item_id",
                "transaction_id",
                "product_id",
                "quantity",
                "price",
            ],
        },
    )

    wait_for_transaction >> load_transaction_items