from airflow.models import DagRun
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
from alerts.google_chat_msg import send_msg
import pendulum 
import yaml
import os

default_args = {
    'owner': 'lakshay',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': [""],
    'email_on_failure': True,
    'email_on_retry': True,
    'email_on_success': True,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
    'trigger_rule': 'none_skipped',
    # 'on_failure_callback': send_msg,
    # 'on_success_callback': send_msg,
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': my_function2,
    # 'on_success_callback': my_function2,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
        
}




from datetime import datetime
def my_function():
    config_files_path = os.getcwd()+"/dags/repo/dags/test_mle/config/"
    files = os.listdir(config_files_path)

    config = {}
    for file in files:
        if "yaml" in file:
            with open(config_files_path + file, "r") as stream:
                try:
                    data = yaml.safe_load(stream)
                    market = data["market_name"]
                    config[market] = data
                    
                except yaml.YAMLError as exc:
                    print(exc)
    for market in config.keys():
        items = config[market]['secrets_names']
        print(items)
    return config

dag = DAG(
    'python_operator_sample',
    default_args=default_args,
    description='How to use the Python Operator?',
    schedule_interval=timedelta(days=1)
)

t2 = PythonOperator(
    task_id='test_job_mle',
    python_callable=my_function,
    dag=dag,
    )
