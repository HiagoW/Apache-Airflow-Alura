import sys
sys.path.append("airflow_pipeline")

from datetime import datetime, timedelta
import json
from os.path import join
from pathlib import Path
from hook.twitter_hook import TwitterHook
from airflow.models import BaseOperator, TaskInstance, DAG

class TwitterOperator(BaseOperator):

    def __init__(self, file_path, end_time, start_time, query, **kwargs):
        self.file_path = file_path
        self.end_time = end_time
        self.start_time = start_time
        self.query = query
        super().__init(**kwargs)

    def create_parent_folder(self):
        (Path(self.file_path).parent).mkdir(parents=True, exist_ok=True)
    
    def execute(self, context):
        end_time = self.end_time
        start_time = self.start_time
        query = self.query

        self.create_parent_folder()

        with open(self.file_path, "w") as output_file:
            for pg in TwitterHook(end_time, start_time, query).run():
                json.dump(pg, output_file, ensure_ascii=False)
                output_file.write("\n")

if __name__ == "__main__":
    TIMESTAMP_FORMAT = f"%Y-%m-%dT%H:%M:%S.00Z"

    end_time = datetime.now().strftime(TIMESTAMP_FORMAT)
    start_time = (datetime.now() + timedelta(-1)).date().strftime(TIMESTAMP_FORMAT)
    query = "data science"

    with DAG(dag_id = "TwitterTest", start_date = datetime.now()) as dag:
        to = TwitterOperator(file_path=join("datalake/twitter_datascience",
                                            f"extract_date={datetime.now().date()}",
                                            f"datascience_{datetime.now().date().strftime('%Y%m%d')}.json"),
                                            end_time=end_time, start_time=start_time, query=query, task_id="test_run")
        ti = TaskInstance(task=to)
        to.execute(ti.task_id)