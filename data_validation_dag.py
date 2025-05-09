from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
import os

# Configuração de caminhos absolutos
HOME = os.path.expanduser("~")
GE_DIR = os.path.join(HOME, "dev/ge_data")
SCRIPTS_DIR = os.path.join(GE_DIR, "scripts")
DATA_DIR = os.path.join(GE_DIR, "data")

# Garante que os diretórios existam
os.makedirs(os.path.join(DATA_DIR, "raw"), exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, "processed"), exist_ok=True)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def generate_data():
    import sys
    sys.path.insert(0, SCRIPTS_DIR)
    from generate_data import generate_customer_data, save_to_txt
    
    today = datetime.now().strftime('%Y%m%d')
    raw_file = os.path.join(DATA_DIR, "raw", f"customers_{today}.txt")
    save_to_txt(generate_customer_data(1000), raw_file)

def transform_data():
    import sys
    sys.path.insert(0, SCRIPTS_DIR)
    from transform_etl import transform_txt_to_csv
    
    today = datetime.now().strftime('%Y%m%d')
    transform_txt_to_csv(
        os.path.join(DATA_DIR, "raw", f"customers_{today}.txt"),
        os.path.join(DATA_DIR, "processed", f"customers_{today}.csv")
    )

with DAG(
    'data_validation_pipeline',
    default_args=default_args,
    description='Pipeline para gerar, transformar e validar dados de clientes',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 5, 1),
    catchup=False,
) as dag:

    start = EmptyOperator(task_id='start')
    
    generate_task = PythonOperator(
        task_id='generate_data',
        python_callable=generate_data,
    )

    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
    )

    validate_task = BashOperator(
        task_id='validate_data',
        bash_command=f"{os.path.join(GE_DIR, 'bin/python')} {os.path.join(SCRIPTS_DIR, 'validation.py')}",
        env={
            "PYTHONPATH": GE_DIR,
            "GE_HOME": GE_DIR,
            "AIRFLOW_DATA_DIR": DATA_DIR
        },
        cwd=GE_DIR  # Define o diretório de trabalho como a raiz do projeto GE
    )

    end = EmptyOperator(task_id='end')

    start >> generate_task >> transform_task >> validate_task >> end