"""Limpieza del dataset crudo de Credit Score.

Cada decisión sale del EDA (notebook 02, reports/01_eda.md):
  1. Se eliminan los datos personales (ID, Name, SSN).
  2. Los valores centinela y la basura de texto ("_", "__10000__", "!@9#%8", ...) pasan a NaN.
  3. Los números con guion bajo sobrante ("23_") se convierten en número.
  4. Los valores fuera de un rango plausible pasan a NaN (no se borran las filas).
  5. Las variables que por naturaleza no cambian de mes a mes (incluida Credit_Mix, que en el EDA
     resultó constante por cliente) se reparan con el valor más frecuente válido del propio cliente.
     Solo usa filas del mismo cliente, así que no cruza particiones.
  6. La antigüedad crediticia sube exactamente un mes por mes: se reconstruye en vez de imputarla.
  7. El sueldo mensual es casi ingreso anual / 12: sus vacíos se rellenan con la mediana del cliente.
  8. Type_of_Loan vacío significa "sin préstamos" (coincide exacto con Num_of_Loan == 0): no se imputa.
"""
import numpy as np
import pandas as pd

from creditsight.config import MONTH_TO_INT, PII_COLUMNS, RAW_CSV

# Cadenas que significan "dato corrupto o no informado", no un valor real
SENTINELS = {"_", "_______", "__10000__", "__-333333333333333333333333333__", "!@9#%8", "#F%$D@*&8"}

# Columnas numéricas guardadas como texto en el CSV
TEXT_NUMERIC = [
    "Age",
    "Annual_Income",
    "Num_of_Loan",
    "Num_of_Delayed_Payment",
    "Changed_Credit_Limit",
    "Outstanding_Debt",
    "Amount_invested_monthly",
    "Monthly_Balance",
]

# Rango plausible (mínimo, máximo) por columna; fuera de él, el valor se considera corrupto.
# Los topes salen de los percentiles del EDA: hay un salto claro entre el 95-97 % de los datos y el resto.
PLAUSIBLE_RANGE = {
    "Age": (14, 100),
    "Annual_Income": (0, 300_000),
    "Num_Bank_Accounts": (0, 11),
    "Num_Credit_Card": (0, 11),
    "Interest_Rate": (0, 34),
    "Num_of_Loan": (0, 9),
    "Num_of_Delayed_Payment": (0, 28),
    "Num_Credit_Inquiries": (0, 17),
    "Total_EMI_per_month": (0, 2_000),
}

# Variables estables por cliente: su valor real no cambia entre meses
STABLE_PER_CUSTOMER = [
    "Age",
    "Occupation",
    "Annual_Income",
    "Num_Bank_Accounts",
    "Num_Credit_Card",
    "Interest_Rate",
    "Num_of_Loan",
    "Credit_Mix",
]


def load_raw(path=RAW_CSV) -> pd.DataFrame:
    """Lee el CSV crudo y elimina los datos personales."""
    return pd.read_csv(path, low_memory=False).drop(columns=PII_COLUMNS)


def _strip_sentinels(df: pd.DataFrame) -> pd.DataFrame:
    """Reemplaza los valores centinela de texto por NaN."""
    text_cols = df.select_dtypes(include=["object", "string"]).columns
    for col in text_cols:
        df[col] = df[col].where(~df[col].isin(SENTINELS))
    return df


def _to_number(series: pd.Series) -> pd.Series:
    """Convierte texto como '23_' o '1,234' en número; lo que no sea número queda en NaN."""
    return pd.to_numeric(series.astype("string").str.strip("_").str.replace(",", "", regex=False), errors="coerce")


def _customer_mode(df: pd.DataFrame, col: str) -> pd.Series:
    """Valor más frecuente (no vacío) de `col` para cada cliente, alineado con las filas de df."""
    counts = df.groupby(["Customer_ID", col], observed=True).size().rename("n").reset_index()
    best = counts.sort_values(["Customer_ID", "n"], ascending=[True, False], kind="stable").drop_duplicates("Customer_ID")
    return df["Customer_ID"].map(best.set_index("Customer_ID")[col])


def parse_credit_history(series: pd.Series) -> pd.Series:
    """'22 Years and 1 Months' -> 265 (meses)."""
    parts = series.str.extract(r"(\d+)\s+Years?\s+and\s+(\d+)\s+Months?").astype(float)
    return parts[0] * 12 + parts[1]


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Devuelve el dataset limpio, con el mismo número de filas que el crudo."""
    df = df.copy()
    df = _strip_sentinels(df)

    for col in TEXT_NUMERIC:
        df[col] = _to_number(df[col]).astype(float)

    for col, (low, high) in PLAUSIBLE_RANGE.items():
        df[col] = df[col].where(df[col].between(low, high))

    # Índice de mes (0..7), necesario para ordenar y para reconstruir la antigüedad
    df["month_idx"] = df["Month"].map(MONTH_TO_INT)

    # Variables estables: valor más frecuente válido de cada cliente
    for col in STABLE_PER_CUSTOMER:
        df[col] = _customer_mode(df, col)

    # Sueldo mensual: casi ingreso anual / 12; los vacíos se rellenan con la mediana del cliente
    df["Monthly_Inhand_Salary"] = df["Monthly_Inhand_Salary"].fillna(
        df.groupby("Customer_ID")["Monthly_Inhand_Salary"].transform("median")
    )

    # Antigüedad crediticia: el desfase (antigüedad - mes) es constante por cliente
    df["Credit_History_Months"] = parse_credit_history(df["Credit_History_Age"])
    offset = (df["Credit_History_Months"] - df["month_idx"]).groupby(df["Customer_ID"]).transform("median")
    df["Credit_History_Months"] = df["Credit_History_Months"].fillna(offset + df["month_idx"])
    df = df.drop(columns=["Credit_History_Age"])

    return df.sort_values(["Customer_ID", "month_idx"]).reset_index(drop=True)
