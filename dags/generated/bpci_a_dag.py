from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='bpci_a_dag',
    default_args=default_args,
    start_date=datetime(2025, 5, 27),
    schedule_interval='@daily',
    catchup=False,
) as dag:

    
    task_1 = BigQueryInsertJobOperator(
        task_id='task_1',
        configuration={
            "query": {
                "query": open("sql/bpci_a/test_1.sql").read(),
                "useLegacySql": False,
            }
        },
        location='US',
    )
    
    task_4 = BigQueryInsertJobOperator(
        task_id='task_4',
        configuration={
            "query": {
                "query": open("sql/bpci_a/test_2.sql").read(),
                "useLegacySql": False,
            }
        },
        location='US',
    )
    
    task_3 = BigQueryInsertJobOperator(
        task_id='task_3',
        configuration={
            "query": {
                "query": open("sql/bpci_a/test_3.sql").read(),
                "useLegacySql": False,
            }
        },
        location='US',
    )
    

    
        
    
        
    
        
    task_1 >> task_3
        
    task_4 >> task_3
        
    