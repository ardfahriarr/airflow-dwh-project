from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.standard.sensors.external_task import ExternalTaskSensor
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SQL_DIR = PROJECT_ROOT / "sql" / "dwh"


with DAG(
    dag_id="fact_sales",
    start_date=datetime(2026, 9, 1),
    schedule="30 1 * * *",
    catchup=False,
    max_active_runs=1,
    tags=["dwh", "fact"],
    template_searchpath=["/opt/airflow/sql"],
) as dag:

    wait_dim_customer = ExternalTaskSensor(
        task_id="wait_dim_customer",
        external_dag_id="dim_customer",
        external_task_id="load_dim_customer",
        execution_delta=timedelta(minutes=30),
        allowed_states=["success"],
        failed_states=["failed"],
        poke_interval=30,
        timeout=3600,
        mode="reschedule",
    )

    wait_dim_product = ExternalTaskSensor(
        task_id="wait_dim_product",
        external_dag_id="dim_product",
        external_task_id="load_dim_product",
        execution_delta=timedelta(minutes=30),
        allowed_states=["success"],
        failed_states=["failed"],
        poke_interval=30,
        timeout=3600,
        mode="reschedule",
    )

    wait_dim_date = ExternalTaskSensor(
        task_id="wait_dim_date",
        external_dag_id="dim_date",
        external_task_id="load_dim_date",
        execution_delta=timedelta(minutes=30),
        allowed_states=["success"],
        failed_states=["failed"],
        poke_interval=30,
        timeout=3600,
        mode="reschedule",
    )

    wait_dim_campaign = ExternalTaskSensor(
        task_id="wait_dim_campaign",
        external_dag_id="dim_campaign",
        external_task_id="load_dim_campaign",
        execution_delta=timedelta(minutes=30),
        allowed_states=["success"],
        failed_states=["failed"],
        poke_interval=30,
        timeout=3600,
        mode="reschedule",
    )

    load_fact_sales = SQLExecuteQueryOperator(
        task_id="load_fact_sales",
        conn_id="postgres_dwh",
        sql="dwh/05_fact_sales.sql",
    )

    [
        wait_dim_customer,
        wait_dim_product,
        wait_dim_date,
        wait_dim_campaign,
    ] >> load_fact_sales