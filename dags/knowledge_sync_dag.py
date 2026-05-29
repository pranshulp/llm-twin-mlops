import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
import subprocess

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def trigger_beam_ingestion():
    """Executes the Beam ingestion script using the venv python."""
    venv_python = os.path.join(PROJECT_ROOT, "venv", "Scripts", "python.exe")
    
    result = subprocess.run(
        [venv_python, "-m", "data_pipeline.beam_ingest"],
        cwd=PROJECT_ROOT, # Run from the root so imports work
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        raise Exception(f"Beam Ingestion Failed: {result.stderr}")
    print(f"Beam Output: {result.stdout}")

default_args = {
    'owner': 'senior_dev',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'llm_twin_sync_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False
) as dag:

    sync_task = PythonOperator(
        task_id='run_parallel_ingestion',
        python_callable=trigger_beam_ingestion
    )