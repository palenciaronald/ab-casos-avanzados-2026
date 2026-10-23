"""Conexión y registro de ejecuciones en MLflow: Databricks si hay conexión, local si no.

Dos formas de conectar a Databricks, ambas leídas de `.env` (ver `.env.example`):
  - PROFILE=<perfil de ~/.databrickscfg>        -> databricks://<perfil>
  - DATABRICKS_HOST + DATABRICKS_TOKEN          -> databricks
Si no hay conexión (o se pide `force_local`), se usa una base SQLite local: el notebook corre igual
y sirve de respaldo cuando se agota la cuota diaria de Databricks Free Edition.
"""
import os
import warnings
from pathlib import Path

import mlflow
from dotenv import load_dotenv

from creditsight.config import EXAMPLE_DIR, ROOT

LOCAL_DB = EXAMPLE_DIR / "mlflow_local.db"  # se genera sola; no se versiona
PLACEHOLDER_PROFILE = "nombre-de-tu-perfil"  # valor de .env.example sin completar


def is_databricks() -> bool:
    """True si el código corre dentro de un workspace de Databricks."""
    return "DATABRICKS_RUNTIME_VERSION" in os.environ


def _reachable() -> bool:
    try:
        mlflow.search_experiments(max_results=1)
        return True
    except Exception as error:  # sin red, credenciales inválidas, cuota agotada, CLI fuera del PATH...
        reason = str(error).splitlines()[0][:140]
        warnings.warn(f"Databricks no disponible ({reason}). Se usa MLflow local.", stacklevel=3)
        return False


def configure_mlflow(force_local: bool = False, local_db: Path = LOCAL_DB, env_file: Path = ROOT / ".env") -> str:
    """Configura MLflow y devuelve una descripción de dónde quedó: 'databricks (...)' o 'local'."""
    if is_databricks() and not force_local:
        return "databricks (dentro del workspace)"
    load_dotenv(env_file)
    if not force_local and os.environ.get("MLFLOW_FORCE_LOCAL") != "1":
        profile = os.environ.get("PROFILE")
        if profile and profile != PLACEHOLDER_PROFILE:
            mlflow.set_tracking_uri(f"databricks://{profile}")
            mlflow.set_registry_uri(f"databricks-uc://{profile}")
            if _reachable():
                return f"databricks (perfil {profile})"
        elif os.environ.get("DATABRICKS_HOST") and os.environ.get("DATABRICKS_TOKEN"):
            mlflow.set_tracking_uri("databricks")
            mlflow.set_registry_uri("databricks-uc")
            if _reachable():
                return "databricks (token)"
    local_uri = f"sqlite:///{Path(local_db).as_posix()}"
    mlflow.set_tracking_uri(local_uri)
    mlflow.set_registry_uri(local_uri)
    return "local"


def uses_databricks() -> bool:
    """True si MLflow quedó apuntando a Databricks (tras `configure_mlflow`)."""
    return mlflow.get_tracking_uri().startswith("databricks")


def _databricks_user() -> str:
    from databricks.sdk import WorkspaceClient

    profile = os.environ.get("PROFILE")
    if profile and profile != PLACEHOLDER_PROFILE and not is_databricks():
        return WorkspaceClient(profile=profile).current_user.me().user_name
    return WorkspaceClient().current_user.me().user_name


def set_experiment(name: str) -> str:
    """Crea o activa el experimento. En Databricks el nombre debe ser una ruta.

    Si `.env` define EXPERIMENT_DIR (una carpeta del workspace que ya existe), el experimento va ahí;
    si no, en /Users/<usuario>/.
    """
    if uses_databricks():
        folder = os.environ.get("EXPERIMENT_DIR", "").rstrip("/") or f"/Users/{_databricks_user()}"
        full_name = f"{folder}/{name}"
    else:
        full_name = name
    mlflow.set_experiment(full_name)
    return full_name


def registered_model_name(name: str) -> str:
    """Nombre completo para el registro: catalog.schema.name en Unity Catalog; el nombre solo en local."""
    if not mlflow.get_registry_uri().startswith("databricks"):
        return name
    catalog = os.environ.get("UC_CATALOG", "workspace")
    schema = os.environ.get("UC_SCHEMA", "default")
    return f"{catalog}.{schema}.{name}"


def log_run(run_name: str, params: dict, metrics: dict, tags: dict | None = None, nested: bool = False) -> str:
    """Registra una ejecución completa (parámetros, métricas y etiquetas) y devuelve su run_id."""
    with mlflow.start_run(run_name=run_name, nested=nested) as run:
        mlflow.log_params({k: ("None" if v is None else v) for k, v in params.items()})
        mlflow.log_metrics({k: float(v) for k, v in metrics.items()})
        if tags:
            mlflow.set_tags(tags)
        return run.info.run_id
