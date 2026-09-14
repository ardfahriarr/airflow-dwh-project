from pathlib import Path
from airflow.providers.postgres.hooks.postgres import PostgresHook

POSTGRES_CONN_ID = "postgres_dwh"
DATA_DIR = Path("/opt/airflow/data/sample")


def load_csv(table_name, file_name, columns, required_columns):

    file_path = DATA_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(file_path)

    hook = PostgresHook(
        postgres_conn_id=POSTGRES_CONN_ID
    )

    conn = hook.get_conn()

    try:
        with conn.cursor() as cursor:

            cursor.execute("""
                CREATE SCHEMA IF NOT EXISTS staging;
            """)

            cursor.execute(f"""
                TRUNCATE TABLE staging.{table_name};
            """)

            with file_path.open("rb") as file:
                with cursor.copy(
                    f"""
                    COPY staging.{table_name}
                    FROM STDIN
                    WITH (FORMAT CSV, HEADER TRUE)
                    """
                ) as copy:
                    while data := file.read(8192):
                        copy.write(data)

            # Count
            cursor.execute(
                f"""
                SELECT COUNT(*)
                FROM staging.{table_name}
                """
            )
            row_count = cursor.fetchone()[0]
            if row_count == 0:
                raise ValueError(
                    f"{table_name}: empty table"
                )
            # Invalid data
            condition = " OR ".join(
                f"{column} IS NULL"
                for column in required_columns
            )
            cursor.execute(
                f"""
                SELECT COUNT(*)
                FROM staging.{table_name}
                WHERE {condition}
                """
            )
            invalid_count = cursor.fetchone()[0]
            valid_count = row_count - invalid_count
            print(
                f"{table_name}: "
                f"total={row_count}, "
                f"valid={valid_count}, "
                f"invalid={invalid_count}"
            )
            if invalid_count > 0:
                raise ValueError(
                    f"{table_name}: "
                    f"{invalid_count} invalid rows"
                )
        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()