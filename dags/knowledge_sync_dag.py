import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def trigger_beam_ingestion():
    """Executes the Beam ingestion script using the venv python."""
    import subprocess
    
    project_root = "/opt/airflow/project_root"
    
    result = subprocess.run(
        ["python3", "-m", "data_pipeline.beam_ingest"],
        cwd=project_root,
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
    schedule='0 0 * * *', # Daily at midnight
    start_date=datetime(2024, 1, 1),
    catchup=False
) as dag:

    sync_task = PythonOperator(
        task_id='run_parallel_ingestion',
        python_callable=trigger_beam_ingestion
    )