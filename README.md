# Getting files from docker

1.
```shell
docker exec -it airflow-alura-airflow-worker-1 bash
#OR
winpty docker exec -it airflow-alura-airflow-worker-1 bash
```

2.
```shell
docker cp airflow-alura-airflow-worker-1:/opt/airflow/semana=2023-09-18 .
```

# Airflow Standalone
```shell
source airflow-venv/bin/activate
export AIRFLOW_HOME=$(pwd)
export SPARK_HOME=/root/spark-3.1.3-bin-hadoop3.2
airflow standalone
```