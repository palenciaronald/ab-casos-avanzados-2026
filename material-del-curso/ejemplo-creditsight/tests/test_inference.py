import numpy as np
import pandas as pd
import pytest
from sklearn.dummy import DummyClassifier
from sklearn.pipeline import Pipeline

from creditsight.inference.predict import InputValidationError, predict, required_columns, validate_inputs


def _row(**kw) -> pd.DataFrame:
    numeric, categorical = required_columns()
    row = {c: 10.0 for c in numeric}
    row.update({"Age": 30, "Annual_Income": 40000, "Num_Bank_Accounts": 3, "Num_Credit_Card": 4,
                "Interest_Rate": 12, "Num_of_Loan": 2, "Num_of_Delayed_Payment": 5, "Num_Credit_Inquiries": 3,
                "Total_EMI_per_month": 100})
    row.update({c: "x" for c in categorical})
    row.update(kw)
    return pd.DataFrame([row])


class _FixedProba:
    """Modelo de juguete que devuelve siempre las mismas probabilidades."""

    def __init__(self, proba):
        self.proba = np.array(proba)

    def predict_proba(self, X):
        return np.tile(self.proba, (len(X), 1))


def test_valid_input_has_no_errors():
    assert validate_inputs(_row()) == []


def test_missing_column_is_an_error_with_its_name():
    with pytest.raises(InputValidationError, match="Annual_Income"):
        validate_inputs(_row().drop(columns=["Annual_Income"]))


def test_implausible_value_is_an_error_not_a_silent_prediction():
    with pytest.raises(InputValidationError, match="Age"):
        predict(_row(Age=-500), model=_FixedProba([0.2, 0.5, 0.3]))


def test_non_numeric_value_is_an_error():
    with pytest.raises(InputValidationError, match="Annual_Income"):
        validate_inputs(_row(Annual_Income="mucho"))


def test_unseen_category_is_a_warning_when_schema_given():
    schema = {"categories": {"Occupation": ["Doctor"]}}
    assert any("Occupation" in w for w in validate_inputs(_row(Occupation="Astronauta"), schema))


def test_predict_uses_min_cost_rule_and_flags_review():
    # 45 % Poor / 45 % Good: la regla de costo nunca decide Good (aprobar) y pide revisión
    result = predict(_row(), model=_FixedProba([0.45, 0.10, 0.45]), schema={})
    assert result["decision"].iloc[0] != "Good"
    assert bool(result["needs_review"].iloc[0])
    assert np.isclose(result[["proba_Poor", "proba_Standard", "proba_Good"]].sum(axis=1).iloc[0], 1.0)


def test_confident_prediction_does_not_need_review():
    result = predict(_row(), model=_FixedProba([0.02, 0.03, 0.95]), schema={})
    assert result["decision"].iloc[0] == "Good" and not bool(result["needs_review"].iloc[0])
