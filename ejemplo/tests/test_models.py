import numpy as np

from creditsight.config import COST_MATRIX
from creditsight.models.train import decide_min_cost, expected_cost, metrics_from_proba


def test_expected_cost_is_zero_for_perfect_predictions():
    y = np.array([0, 1, 2, 1])
    assert expected_cost(y, y) == 0.0


def test_expected_cost_uses_the_cost_matrix():
    # real Poor (0) predicho Good (2) cuesta 10; real Good (2) predicho Poor (0) cuesta 2
    assert expected_cost(np.array([0]), np.array([2])) == COST_MATRIX[0, 2] == 10
    assert expected_cost(np.array([2]), np.array([0])) == COST_MATRIX[2, 0] == 2


def test_decision_rule_prefers_the_cheaper_error_when_unsure():
    # 45 % Poor, 10 % Standard, 45 % Good: argmax duda entre Poor y Good, pero predecir Good es muy caro si era Poor
    proba = np.array([[0.45, 0.10, 0.45]])
    assert decide_min_cost(proba)[0] != 2  # nunca aprueba (Good) con esa incertidumbre


def test_decision_rule_matches_argmax_when_confident():
    proba = np.array([[0.98, 0.01, 0.01], [0.01, 0.01, 0.98]])
    assert decide_min_cost(proba).tolist() == [0, 2]


def test_metrics_from_proba_returns_both_decision_rules():
    y = np.array([0, 1, 2, 1, 0, 2])
    proba = np.full((6, 3), 1 / 3)
    result = metrics_from_proba(y, proba)
    assert {"cost", "cost_argmax", "macro_f1", "macro_f1_argmax", "recall_poor", "log_loss"} <= set(result)
    assert result["cost"] <= result["cost_argmax"] + 1e-9  # la regla de costo nunca es peor con probabilidades uniformes
