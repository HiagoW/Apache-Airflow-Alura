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
```

* 