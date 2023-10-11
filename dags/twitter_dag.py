from pathlib import Path
import sys
sys.path.append("/mnt/c/Users/Pichau/Desktop/airflow-alura")

from operators.twitter_operator import TwitterOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator;
from airflow.models import TaskInstance, DAG
from datetime import datetime, timedelta
from os.path import join
from airflow.utils.dates import days_ago

with DAG(dag_id = "TwitterDAG", start_date = days_ago(2), schedule_interval="@daily") as dag:
    BASE_FOLDER = join(
       str(Path("/mnt/c/Users/Pichau/Desktop").expanduser()),
       "airflow-alura/datalake/{stage}/twitter_datascience/{partition}",
    )
    PARTITION_FOLDER_EXTRACT = "extract_date={{ data_interval_start.strftime('%Y-%m-%d') }}"
    TIMESTAMP_FORMAT = f"%Y-%m-%dT%H:%M:%S.00Z"
    end_time = datetime.now().strftime(TIMESTAMP_FORMAT)
    start_time = (datetime.now() + timedelta(-1)).date().strftime(TIMESTAMP_FORMAT)

    query = "data science"
    
    twitter_operator = TwitterOperator(file_path=join(BASE_FOLDER.format(stage="Bronze", partition=PARTITION_FOLDER_EXTRACT),
                                        "datascience_{{ ds_nodash }}.json"),
                                        start_time="{{ data_interval_start.strftime('%Y-%m-%dT%H:%M:%S.00Z') }}",
                                        end_time="{{ data_interval_end.strftime('%Y-%m-%dT%H:%M:%S.00Z') }}",
                                        query=query, 
                                        task_id="twitter_datascience")
    
    twitter_transform = SparkSubmitOperator(task_id="transform_twitter_datascience",
                                            application="spark/transformation.py",
                                            name="twitter_transformation",
                                            application_args=["--src", BASE_FOLDER.format(stage="Bronze", partition=PARTITION_FOLDER_EXTRACT), 
                                                              "--dest", BASE_FOLDER.format(stage="Silver", partition=""),
                                                              "--process-date", "{{ ds }}"])
    
    twitter_insight = SparkSubmitOperator(task_id="insight_twitter",
                                            application="spark/insight_tweet.py",
                                            name="insight_twitter",
                                            application_args=["--src", BASE_FOLDER.format(stage="Silver", partition=""), 
                                                              "--dest", BASE_FOLDER.format(stage="Gold", partition=""),
                                                              "--process-date", "{{ ds }}"])
    
    twitter_operator >> twitter_transform >> twitter_insight