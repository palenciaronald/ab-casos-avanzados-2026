"""Constantes del proyecto CreditSight: rutas, columnas, objetivo y matriz de costos."""
from pathlib import Path

import numpy as np

# ejemplo/src/creditsight/config.py -> la raíz del repo está tres niveles arriba de ejemplo/src
ROOT = Path(__file__).resolve().parents[3]
EXAMPLE_DIR = ROOT / "ejemplo"
RAW_CSV = ROOT / "data" / "01-clasificacion" / "credit_score_classification.csv"
PROCESSED_DIR = EXAMPLE_DIR / "data_processed"  # se regenera con el notebook 03; no se versiona
MODELS_DIR = EXAMPLE_DIR / "models"
REPORTS_DIR = EXAMPLE_DIR / "reports"

RANDOM_STATE = 42
GROUP_COL = "Customer_ID"  # unidad de análisis para particionar: el cliente, no la fila
TARGET = "Credit_Score"

# Orden de riesgo: 0 = peor perfil, 2 = mejor perfil
CLASSES = ["Poor", "Standard", "Good"]
CLASS_TO_INT = {name: i for i, name in enumerate(CLASSES)}

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August"]
MONTH_TO_INT = {name: i for i, name in enumerate(MONTHS)}

# Datos personales: se eliminan al cargar, nunca llegan al modelo
PII_COLUMNS = ["ID", "Name", "SSN"]

# Matriz de costos de equivocarse: filas = clase real, columnas = clase predicha (orden CLASSES).
# Aprobar crédito a un cliente riesgoso cuesta mucho más que rechazar a uno bueno.
COST_MATRIX = np.array(
    [
        [0, 3, 10],  # real Poor:     predice Poor / Standard / Good
        [1, 0, 3],  # real Standard
        [2, 1, 0],  # real Good
    ],
    dtype=float,
)
