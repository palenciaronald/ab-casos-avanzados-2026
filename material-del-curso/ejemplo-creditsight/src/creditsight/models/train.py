"""Candidatos, métricas con costo de negocio y evaluación con validación cruzada por cliente."""
import time

import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.base import clone
from sklearn.metrics import f1_score, log_loss, recall_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from xgboost import XGBClassifier

from creditsight.config import CLASS_TO_INT, COST_MATRIX, GROUP_COL, RANDOM_STATE, TARGET
from creditsight.features.engineering import add_features, build_preprocessor


def encode_target(y: pd.Series) -> np.ndarray:
    """Poor/Standard/Good -> 0/1/2."""
    return y.map(CLASS_TO_INT).to_numpy()


def expected_cost(y_true, y_pred, cost: np.ndarray = COST_MATRIX) -> float:
    """Costo promedio por cliente-mes según la matriz de costos (menor es mejor)."""
    return float(cost[np.asarray(y_true), np.asarray(y_pred)].mean())


def decide_min_cost(proba: np.ndarray, cost: np.ndarray = COST_MATRIX) -> np.ndarray:
    """Elige la clase con menor costo esperado: argmin_j sum_i p_i * costo(i, j).

    Con probabilidades bien calibradas esto es la decisión óptima para esa matriz de costos.
    """
    return np.argmin(proba @ cost, axis=1)


def candidates(random_state: int = RANDOM_STATE) -> dict:
    """Modelos del torneo; el booleano indica si necesitan variables escaladas."""
    return {
        "baseline (clase más frecuente)": (DummyClassifier(strategy="most_frequent"), False),
        "regresión logística": (LogisticRegression(max_iter=1000, random_state=random_state), True),
        "random forest": (
            RandomForestClassifier(n_estimators=200, min_samples_leaf=3, n_jobs=-1, random_state=random_state),
            False,
        ),
        "lightgbm": (
            LGBMClassifier(n_estimators=300, learning_rate=0.05, num_leaves=31, random_state=random_state, verbose=-1),
            False,
        ),
        "xgboost": (
            XGBClassifier(
                n_estimators=300, learning_rate=0.05, max_depth=6, tree_method="hist",
                random_state=random_state, n_jobs=-1, eval_metric="mlogloss",
            ),
            False,
        ),
    }


def build_pipeline(
    model,
    scale: bool,
    use_credit_mix: bool = True,
    use_engineered: bool = False,
    extra_numeric: list[str] | None = None,
) -> Pipeline:
    """Pipeline completo: (variables nuevas) -> preprocesamiento -> modelo. Se guarda entero."""
    steps = []
    if use_engineered:
        steps.append(("features", FunctionTransformer(add_features)))
    steps.append(
        (
            "prep",
            build_preprocessor(
                use_credit_mix=use_credit_mix, scale=scale, use_engineered=use_engineered, extra_numeric=extra_numeric
            ),
        )
    )
    steps.append(("model", model))
    return Pipeline(steps)


def metrics_from_proba(y_true: np.ndarray, proba: np.ndarray) -> dict:
    """Métricas de un conjunto de predicciones, con las dos reglas de decisión.

    - *argmax*: la clase más probable.
    - *decision*: la clase de menor costo esperado (la que usa el negocio).
    El costo principal es el de la regla de decisión; el de argmax se reporta para compararla.
    """
    y_true = np.asarray(y_true)
    argmax = proba.argmax(axis=1)
    decision = decide_min_cost(proba)
    return {
        "cost": expected_cost(y_true, decision),
        "cost_argmax": expected_cost(y_true, argmax),
        "macro_f1": f1_score(y_true, decision, average="macro"),
        "macro_f1_argmax": f1_score(y_true, argmax, average="macro"),
        "recall_poor": recall_score(y_true, decision, labels=[0], average="macro"),
        "log_loss": log_loss(y_true, proba, labels=[0, 1, 2]),
    }


def evaluate_folds(pipeline, X: pd.DataFrame, y: np.ndarray, cv) -> pd.DataFrame:
    """Validación cruzada por cliente. Una fila por pliegue con todas las métricas y el tiempo de ajuste."""
    rows = []
    for fold, (train_idx, valid_idx) in enumerate(cv.split(X, y, groups=X[GROUP_COL])):
        model = clone(pipeline)
        start = time.time()
        model.fit(X.iloc[train_idx], y[train_idx])
        seconds = time.time() - start
        rows.append({"fold": fold, **metrics_from_proba(y[valid_idx], model.predict_proba(X.iloc[valid_idx])), "fit_seconds": seconds})
    return pd.DataFrame(rows).set_index("fold")


def evaluate(pipeline, X: pd.DataFrame, y: np.ndarray, cv) -> dict:
    """Como `evaluate_folds`, pero devuelve la media y la desviación entre pliegues de cada métrica."""
    table = evaluate_folds(pipeline, X, y, cv)
    out = {f"{name}_mean": float(table[name].mean()) for name in table if name != "fit_seconds"}
    out.update({f"{name}_std": float(table[name].std()) for name in table if name != "fit_seconds"})
    out["fit_seconds"] = float(table["fit_seconds"].mean())
    return out


def feature_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Quita el objetivo; conserva Customer_ID para poder agrupar (el preprocesamiento lo ignora)."""
    return df.drop(columns=[TARGET])
