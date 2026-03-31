from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime

from src.ingestion.dataextract import run_ingestion
from src.transformation.silver import run_silver
from src.modeling.model import run_modeling
from DB.analytics.queries import run_queries

default_args = {
    "owner": "alex",
    "retries": 1
}

with DAG(
    dag_id="energy_data_pipeline",
    default_args=default_args,
    description="End-to-end data pipeline for ONS data",
    schedule="daily",
    start_date=datetime(2024, 1, 1),
    catchup=False
) as dag:

    ingestion_task = PythonOperator(
        task_id="ingestion",
        python_callable=run_ingestion
    )

    silver_task = PythonOperator(
        task_id="silver",
        python_callable=run_silver
    )

    modeling_task = PythonOperator(
        task_id="modeling",
        python_callable=run_modeling
    )

    analytics_task = PythonOperator(
        task_id="analytics",
        python_callable=run_queries
    )

    ingestion_task >> silver_task >> modeling_task >> analytics_task

