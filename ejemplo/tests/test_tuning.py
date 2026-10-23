import numpy as np

from creditsight.models.tuning import bootstrap_cost_difference


def test_bootstrap_difference_is_zero_for_identical_models():
    rng = np.random.default_rng(0)
    y = rng.integers(0, 3, 400)
    proba = rng.dirichlet(np.ones(3), 400)
    groups = np.repeat(np.arange(50), 8)
    diff, low, high = bootstrap_cost_difference(y, proba, proba, groups, n_boot=200)
    assert diff == 0 and low == 0 and high == 0


def test_bootstrap_detects_a_clearly_better_model_with_negative_difference():
    rng = np.random.default_rng(1)
    y = rng.integers(0, 3, 800)
    good = np.eye(3)[y] * 0.9 + 0.05            # casi siempre acierta
    bad = np.eye(3)[(y + 1) % 3] * 0.9 + 0.05   # casi siempre se equivoca
    groups = np.repeat(np.arange(100), 8)
    diff, low, high = bootstrap_cost_difference(y, good, bad, groups, n_boot=300)
    assert diff < 0 and high < 0  # el intervalo completo está debajo de cero: A es mejor
