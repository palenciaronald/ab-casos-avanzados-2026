"""Partición de datos por cliente.

Cada cliente aparece en 8 meses. Si se parte por fila, los meses de un mismo cliente caen a ambos
lados de la partición y la métrica sale inflada (fuga de información). Aquí **todas** las
particiones respetan al cliente completo.
"""
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit, StratifiedGroupKFold

from creditsight.config import GROUP_COL, RANDOM_STATE


def split_by_customer(df: pd.DataFrame, test_size: float = 0.2, seed: int = RANDOM_STATE):
    """Separa entrenamiento y prueba sin repartir a ningún cliente entre los dos."""
    splitter = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=seed)
    train_idx, test_idx = next(splitter.split(df, groups=df[GROUP_COL]))
    train = df.iloc[train_idx].reset_index(drop=True)
    test = df.iloc[test_idx].reset_index(drop=True)
    assert_disjoint_customers(train, test)
    return train, test


def assert_disjoint_customers(*frames: pd.DataFrame) -> None:
    """Falla si algún cliente aparece en más de una partición."""
    seen: set = set()
    for i, frame in enumerate(frames):
        customers = set(frame[GROUP_COL])
        overlap = seen & customers
        if overlap:
            raise AssertionError(f"{len(overlap)} clientes aparecen en más de una partición (partición {i})")
        seen |= customers


def group_cv(n_splits: int = 5, seed: int = RANDOM_STATE) -> StratifiedGroupKFold:
    """Validación cruzada que mantiene a cada cliente completo en un solo pliegue."""
    return StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=seed)
