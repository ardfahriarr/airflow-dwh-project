from datetime import datetime

from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SQL_DIR = PROJECT_ROOT / "sql" / "dwh"

with DAG(
    dag_id="dim_customer",
    start_date=datetime(2026, 9, 1),
    schedule="0 1 * * *",
    catchup=False,
    max_active_runs=1,
    tags=["dwh", "dimension"],
    template_searchpath=["/opt/airflow/sql"],
) as dag:

    load_dim_customer = SQLExecuteQueryOperator(
        task_id="load_dim_customer",
        conn_id="postgres_dwh",
        sql="dwh/01_dim_customer.sql"
    )