"""Variables nuevas y preprocesamiento.

`add_features` solo usa columnas del mes actual: así el modelo puede predecir con lo que se conoce
en ese momento. En el notebook 04 se midió que estas variables NO mejoran el modelo, por eso el
pipeline final las deja apagadas (`use_engineered=False`); el código se conserva porque documenta
la prueba y porque en otro dataset podrían servir.
"""
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

LOAN_TYPES = [
    "Auto Loan",
    "Credit-Builder Loan",
    "Debt Consolidation Loan",
    "Home Equity Loan",
    "Mortgage Loan",
    "Payday Loan",
    "Personal Loan",
    "Student Loan",
]

NUMERIC_BASE = [
    "Age",
    "Annual_Income",
    "Monthly_Inhand_Salary",
    "Num_Bank_Accounts",
    "Num_Credit_Card",
    "Interest_Rate",
    "Num_of_Loan",
    "Delay_from_due_date",
    "Num_of_Delayed_Payment",
    "Changed_Credit_Limit",
    "Num_Credit_Inquiries",
    "Outstanding_Debt",
    "Credit_Utilization_Ratio",
    "Credit_History_Months",
    "Total_EMI_per_month",
    "Amount_invested_monthly",
    "Monthly_Balance",
]
NUMERIC_ENGINEERED = [
    "debt_to_income",
    "emi_to_salary",
    "invested_to_salary",
    "balance_to_salary",
    "n_loan_types",
] + [f"loan_{i}" for i in range(len(LOAN_TYPES))]
CATEGORICAL_BASE = ["Occupation", "Payment_of_Min_Amount", "Payment_Behaviour"]
CREDIT_MIX = "Credit_Mix"


def _ratio(num: pd.Series, den: pd.Series) -> pd.Series:
    """División segura: denominador cero o ausente -> NaN."""
    return num / den.where(den > 0)


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Añade razones financieras y marcas de tipo de préstamo. No modifica el original."""
    out = df.copy()
    out["debt_to_income"] = _ratio(out["Outstanding_Debt"], out["Annual_Income"])
    out["emi_to_salary"] = _ratio(out["Total_EMI_per_month"], out["Monthly_Inhand_Salary"])
    out["invested_to_salary"] = _ratio(out["Amount_invested_monthly"], out["Monthly_Inhand_Salary"])
    out["balance_to_salary"] = _ratio(out["Monthly_Balance"], out["Monthly_Inhand_Salary"])

    loans = out["Type_of_Loan"].fillna("")
    for i, loan_type in enumerate(LOAN_TYPES):
        out[f"loan_{i}"] = loans.str.contains(loan_type, regex=False).astype(float)
    out["n_loan_types"] = out[[f"loan_{i}" for i in range(len(LOAN_TYPES))]].sum(axis=1)
    return out


def feature_columns(
    use_credit_mix: bool = True, use_engineered: bool = False, extra_numeric: list[str] | None = None
) -> tuple[list[str], list[str]]:
    """Devuelve (numéricas, categóricas) que usa el modelo.

    `extra_numeric` permite probar columnas adicionales (p. ej. historial del cliente) sin tocar el código.
    """
    categorical = CATEGORICAL_BASE + ([CREDIT_MIX] if use_credit_mix else [])
    numeric = NUMERIC_BASE + (NUMERIC_ENGINEERED if use_engineered else []) + list(extra_numeric or [])
    return numeric, categorical


def build_preprocessor(
    use_credit_mix: bool = True,
    scale: bool = True,
    use_engineered: bool = False,
    extra_numeric: list[str] | None = None,
) -> ColumnTransformer:
    """Imputación + escalado de numéricas y one-hot de categóricas, ajustados solo con entrenamiento."""
    numeric, categorical = feature_columns(use_credit_mix, use_engineered, extra_numeric)
    numeric_steps = [("impute", SimpleImputer(strategy="median", add_indicator=True))]
    if scale:
        numeric_steps.append(("scale", StandardScaler()))
    categorical_steps = [
        ("impute", SimpleImputer(strategy="constant", fill_value="Unknown")),
        ("onehot", OneHotEncoder(handle_unknown="infrequent_if_exist", min_frequency=0.01, sparse_output=False)),
    ]
    return ColumnTransformer(
        [
            ("num", Pipeline(numeric_steps), numeric),
            ("cat", Pipeline(categorical_steps), categorical),
        ],
        remainder="drop",
    )
