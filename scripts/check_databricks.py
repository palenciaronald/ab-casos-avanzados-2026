"""Comprueba la conexión con Databricks: crea un experimento, registra una ejecución y un modelo.

Uso (desde la raíz del repo, con el entorno activado y el archivo .env completo):

    python scripts/check_databricks.py

Dos formas de conectar, según lo que haya en .env:
  - PROFILE=<perfil de ~/.databrickscfg>        -> databricks://<perfil>
  - DATABRICKS_HOST + DATABRICKS_TOKEN          -> databricks
Dentro de Databricks (DATABRICKS_RUNTIME_VERSION) no se configura nada.
"""
import os
import sys
from pathlib import Path

import mlflow
import numpy as np
from dotenv import load_dotenv
from sklearn.linear_model import LogisticRegression

MODEL_NAME = "curso_v2_prueba"


def is_databricks() -> bool:
    return "DATABRICKS_RUNTIME_VERSION" in os.environ


def configure_mlflow() -> str:
    """Configura MLflow según .env y devuelve una descripción de la conexión."""
    if is_databricks():
        return "dentro de Databricks (sin configuración)"
    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
    profile = os.environ.get("PROFILE")
    if profile and profile != "nombre-de-tu-perfil":
        mlflow.set_tracking_uri(f"databricks://{profile}")
        mlflow.set_registry_uri(f"databricks-uc://{profile}")
        return f"perfil '{profile}'"
    if os.environ.get("DATABRICKS_HOST") and os.environ.get("DATABRICKS_TOKEN"):
        mlflow.set_tracking_uri("databricks")
        mlflow.set_registry_uri("databricks-uc")
        return "token personal"
    sys.exit("Falta configuración: define PROFILE, o DATABRICKS_HOST y DATABRICKS_TOKEN, en el archivo .env")


def current_user() -> str:
    from databricks.sdk import WorkspaceClient

    profile = os.environ.get("PROFILE")
    client = WorkspaceClient(profile=profile) if profile and not is_databricks() else WorkspaceClient()
    return client.current_user.me().user_name


def main() -> None:
    print("Conexión:", configure_mlflow())
    user = current_user()
    print("Usuario:", user)

    mlflow.set_experiment(f"/Users/{user}/curso-v2-prueba")
    with mlflow.start_run(run_name="comprobacion") as run:
        mlflow.log_param("alpha", 0.1)
        mlflow.log_metric("auc", 0.9)
        print("Ejecución registrada:", run.info.run_id)

    rng = np.random.default_rng(0)
    X = rng.random((50, 3))
    y = (X[:, 0] > 0.5).astype(int)
    with mlflow.start_run(run_name="comprobacion-registro"):
        model = LogisticRegression().fit(X, y)
        mlflow.sklearn.log_model(
            model,
            "model",
            registered_model_name=f"workspace.default.{MODEL_NAME}",
            input_example=X[:2],
        )
    print(f"Modelo registrado: workspace.default.{MODEL_NAME}")
    print("OK: el seguimiento y el registro funcionan.")


if __name__ == "__main__":
    main()
