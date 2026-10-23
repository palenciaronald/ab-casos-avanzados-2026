import mlflow

from creditsight.tracking import mlflow_utils as mu


def test_force_local_uses_sqlite_and_logs_a_run(tmp_path):
    where = mu.configure_mlflow(force_local=True, local_db=tmp_path / "mlflow.db", env_file=tmp_path / "no_existe.env")
    assert where == "local"
    assert mlflow.get_tracking_uri().startswith("sqlite:///")
    assert not mu.uses_databricks()

    mu.set_experiment("prueba-local")
    run_id = mu.log_run("r1", {"alpha": 0.1, "depth": None}, {"cost": 0.5}, tags={"etapa": "test"})
    run = mlflow.get_run(run_id)
    assert run.data.params == {"alpha": "0.1", "depth": "None"}
    assert run.data.metrics["cost"] == 0.5
    assert run.data.tags["etapa"] == "test"


def test_registered_model_name_is_plain_when_local(tmp_path):
    mu.configure_mlflow(force_local=True, local_db=tmp_path / "mlflow.db", env_file=tmp_path / "no_existe.env")
    assert mu.registered_model_name("credit_sight") == "credit_sight"


def test_missing_credentials_fall_back_to_local(tmp_path, monkeypatch):
    for var in ("PROFILE", "DATABRICKS_HOST", "DATABRICKS_TOKEN", "MLFLOW_FORCE_LOCAL"):
        monkeypatch.delenv(var, raising=False)
    where = mu.configure_mlflow(local_db=tmp_path / "mlflow.db", env_file=tmp_path / "no_existe.env")
    assert where == "local"


def test_experiment_dir_is_ignored_in_local_mode(tmp_path, monkeypatch):
    monkeypatch.setenv("EXPERIMENT_DIR", "/Users/alguien/carpeta")
    mu.configure_mlflow(force_local=True, local_db=tmp_path / "mlflow.db", env_file=tmp_path / "no_existe.env")
    assert mu.set_experiment("prueba") == "prueba"
