"""Inferencia: validar entradas crudas y predecir con la regla de menor costo esperado.

Contrato (specs/001-curso-v2-end-to-end/contracts/inferencia-app.md):
  - Entrada: columnas crudas que un analista conoce al decidir (ver `required_columns`).
  - Salida: clase decidida, probabilidad por clase y una señal de "revisar" cuando el modelo duda.
  - Nunca devuelve una predicción silenciosa con datos inválidos: lanza `InputValidationError`.
"""
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from creditsight.config import CLASSES, COST_MATRIX, MODELS_DIR
from creditsight.data.cleaning import PLAUSIBLE_RANGE
from creditsight.features.engineering import feature_columns
from creditsight.models.train import decide_min_cost

MODEL_PATH = MODELS_DIR / "model.joblib"
SCHEMA_PATH = MODELS_DIR / "input_schema.json"
REVIEW_THRESHOLD = 0.55  # probabilidad máxima por debajo de la cual se pide revisión humana


class InputValidationError(ValueError):
    """Los datos de entrada no son válidos; el mensaje dice qué corregir."""


def required_columns() -> tuple[list[str], list[str]]:
    """(numéricas, categóricas) que el modelo necesita."""
    return feature_columns(use_credit_mix=True)


def load_schema(path: Path = SCHEMA_PATH) -> dict:
    """Esquema de entrada generado en el notebook 09 (rangos observados y categorías conocidas)."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_model(path: Path = MODEL_PATH):
    return joblib.load(path)


def validate_inputs(df: pd.DataFrame, schema: dict | None = None) -> list[str]:
    """Valida columnas y rangos. Lanza InputValidationError si hay errores; devuelve advertencias."""
    numeric, categorical = required_columns()
    errors, warnings = [], []

    missing = [c for c in numeric + categorical if c not in df.columns]
    if missing:
        raise InputValidationError(f"Faltan columnas: {', '.join(missing)}")

    for col in numeric:
        values = pd.to_numeric(df[col], errors="coerce")
        not_number = values.isna() & df[col].notna()
        if not_number.any():
            errors.append(f"{col}: hay valores que no son números")
        if col in PLAUSIBLE_RANGE:
            low, high = PLAUSIBLE_RANGE[col]
            bad = values.notna() & ~values.between(low, high)
            if bad.any():
                errors.append(f"{col}: debe estar entre {low} y {high}")
    if errors:
        raise InputValidationError("; ".join(errors))

    if schema:
        for col, known in schema.get("categories", {}).items():
            if col in df.columns:
                unseen = set(df[col].dropna().astype(str)) - set(known)
                if unseen:
                    warnings.append(f"{col}: categoría no vista en el entrenamiento ({', '.join(sorted(unseen))})")
        for col, (low, high) in schema.get("observed_range", {}).items():
            if col in df.columns:
                values = pd.to_numeric(df[col], errors="coerce")
                if ((values < low) | (values > high)).any():
                    warnings.append(f"{col}: fuera del rango visto en el entrenamiento ({low:.4g} a {high:.4g})")
    return warnings


def predict(df: pd.DataFrame, model=None, schema: dict | None = None) -> pd.DataFrame:
    """Predice con la regla de menor costo esperado. Una fila de salida por fila de entrada."""
    model = model if model is not None else load_model()
    if schema is None and SCHEMA_PATH.exists():
        schema = load_schema()
    warnings = validate_inputs(df, schema)

    proba = model.predict_proba(df)
    decision = decide_min_cost(proba)
    expected_costs = proba @ COST_MATRIX  # costo esperado de decidir cada clase

    out = pd.DataFrame(proba, columns=[f"proba_{c}" for c in CLASSES], index=df.index)
    out.insert(0, "decision", [CLASSES[i] for i in decision])
    out["most_likely"] = [CLASSES[i] for i in proba.argmax(axis=1)]
    out["expected_cost"] = expected_costs[np.arange(len(df)), decision]
    out["needs_review"] = (proba.max(axis=1) < REVIEW_THRESHOLD) | (decision != proba.argmax(axis=1))
    out.attrs["warnings"] = warnings
    return out
