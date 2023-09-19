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