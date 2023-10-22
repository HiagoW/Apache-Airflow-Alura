```shell
sudo service docker start
minikube start
minikube dashboard
minikube kubectl -- apply -f airflow-config.yml
# If it wrongly tag PVCs to PVs, remove them and run command again

# Open separate tabs:
minikube mount ./dags/:/data/dags
minikube mount ./logs/:/data/logs
minikube mount ./data/:/data/data
minikube ssh
ll /data/dags

eval $(minikube -p minikube docker-env)
docker build -t airflow-alura .
helm upgrade --install airflow apache-airflow/airflow --namespace airflow -f override-values.yml
minikube kubectl -- port-forward svc/airflow-webserver 8080:8080 --namespace airflow
```
 