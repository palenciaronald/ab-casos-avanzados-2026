"""Optimización de hiperparámetros con Optuna, registrando cada ensayo en MLflow."""
import mlflow
import numpy as np
import optuna
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.ensemble import RandomForestClassifier

from creditsight.config import COST_MATRIX, RANDOM_STATE
from creditsight.models.train import build_pipeline, decide_min_cost, evaluate_folds
from creditsight.tracking.mlflow_utils import log_run


def lgbm_space(trial: optuna.Trial) -> dict:
    """Espacio de búsqueda de LightGBM; los rangos salen del conocimiento del algoritmo, no al azar."""
    return {
        "n_estimators": trial.suggest_int("n_estimators", 150, 400),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.2, log=True),
        "num_leaves": trial.suggest_int("num_leaves", 15, 63),
        "min_child_samples": trial.suggest_int("min_child_samples", 20, 200),
        "subsample": trial.suggest_float("subsample", 0.6, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.5, 1.0),
        "reg_lambda": trial.suggest_float("reg_lambda", 1e-3, 10.0, log=True),
    }


def rf_space(trial: optuna.Trial) -> dict:
    """Espacio de búsqueda de random forest. Los árboles se fijan en 200: lo que se afina es su forma."""
    return {
        "max_depth": trial.suggest_int("max_depth", 6, 24),
        "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 20),
        "max_features": trial.suggest_float("max_features", 0.2, 1.0),
    }


def make_lgbm(params: dict, random_state: int = RANDOM_STATE) -> LGBMClassifier:
    return LGBMClassifier(subsample_freq=1, random_state=random_state, verbose=-1, **params)


def make_rf(params: dict, random_state: int = RANDOM_STATE) -> RandomForestClassifier:
    return RandomForestClassifier(n_estimators=200, n_jobs=-1, random_state=random_state, **params)


MODELS = {
    "lightgbm": (lgbm_space, make_lgbm, False),
    "random forest": (rf_space, make_rf, False),
}


def tune(name: str, X: pd.DataFrame, y: np.ndarray, cv, n_trials: int, seed: int = RANDOM_STATE, log: bool = True):
    """Corre un estudio de Optuna que minimiza el costo esperado. Cada ensayo queda como ejecución anidada en MLflow."""
    space_fn, make_fn, scale = MODELS[name]

    def objective(trial: optuna.Trial) -> float:
        params = space_fn(trial)
        folds = evaluate_folds(build_pipeline(make_fn(params), scale=scale), X, y, cv)
        trial.set_user_attr("cost_std", float(folds.cost.std()))
        trial.set_user_attr("log_loss", float(folds.log_loss.mean()))
        if log:
            log_run(
                f"{name}-trial-{trial.number}",
                params,
                {"cost": folds.cost.mean(), "cost_std": folds.cost.std(), "log_loss": folds.log_loss.mean(),
                 "macro_f1": folds.macro_f1.mean(), "recall_poor": folds.recall_poor.mean(),
                 "fit_seconds": folds.fit_seconds.mean()},
                tags={"etapa": "06_optimizacion", "modelo": name},
                nested=True,
            )
        return float(folds.cost.mean())

    study = optuna.create_study(direction="minimize", sampler=optuna.samplers.TPESampler(seed=seed))
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    if log:
        with mlflow.start_run(run_name=f"optuna-{name}") as parent:
            study.optimize(objective, n_trials=n_trials)
            mlflow.log_metric("best_cost", study.best_value)
            mlflow.log_params({f"best_{k}": v for k, v in study.best_params.items()})
            mlflow.set_tags({"etapa": "06_optimizacion", "modelo": name})
            study.set_user_attr("mlflow_parent_run_id", parent.info.run_id)
    else:
        study.optimize(objective, n_trials=n_trials)
    return study


def bootstrap_cost_difference(y_true, proba_a, proba_b, groups, n_boot: int = 1000, seed: int = RANDOM_STATE):
    """Diferencia de costo (A menos B) con intervalo del 95 %, remuestreando CLIENTES completos.

    Remuestrear filas sería otra fuga: los 8 meses de un cliente no son independientes.
    Un valor negativo significa que A cuesta menos que B.
    """
    y_true = np.asarray(y_true)
    cost_a = COST_MATRIX[y_true, decide_min_cost(proba_a)]
    cost_b = COST_MATRIX[y_true, decide_min_cost(proba_b)]
    per_customer = pd.DataFrame({"g": np.asarray(groups), "diff": cost_a - cost_b}).groupby("g")["diff"].agg(["sum", "count"])
    sums, counts = per_customer["sum"].to_numpy(), per_customer["count"].to_numpy()
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(sums), size=(n_boot, len(sums)))
    boot = sums[idx].sum(axis=1) / counts[idx].sum(axis=1)
    return float(sums.sum() / counts.sum()), float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))
