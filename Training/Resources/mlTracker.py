import os
import time
import mlflow
from mlflow.tracking import MlflowClient



#Constantes
MLFLOW_EXPERIMENT_LOCATION = "mlruns"
RUN_BASE_FORMAT = "%Y-%m-%d_%H-%M-%S"

#Ruta al directorio de MLflow
cwd = os.getcwd()
parent = os.path.dirname(cwd)
mlflow_home = os.path.join(parent, MLFLOW_EXPERIMENT_LOCATION)

#Establecer la variable de entorno MLFLOW_HOME
os.environ["MLFLOW_HOME"] = mlflow_home

#Configurar MLflow
mlflow.set_tracking_uri(f"file://{mlflow_home}")

#Funciones

def get_run_id(experiment_name, run_name_tag):
    client = MlflowClient()
    experiment_id = client.get_experiment_by_name(experiment_name).experiment_id
    #Filtrando por tag
    filter_string = f"tags.mlflow.runName = '{run_name_tag}'"
    runs = client.search_runs(experiment_ids=[experiment_id], filter_string=filter_string)
    if runs:
        return runs[0].info.run_id
    else:
        return None
