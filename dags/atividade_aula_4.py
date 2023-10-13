from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

def cumprimentos():
        print("Boas-vindas ao Airflow!")

with DAG(
    'atividade_aula_4',
    start_date=days_ago(1),
    schedule_interval='@daily'
) as dag:
    
    tarefa_python = PythonOperator(task_id = 'atv_4', python_callable = cumprimentos)

