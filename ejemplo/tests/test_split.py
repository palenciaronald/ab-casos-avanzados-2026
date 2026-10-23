import numpy as np
import pandas as pd
import pytest

from creditsight.data.split import assert_disjoint_customers, group_cv, split_by_customer


def _panel(n_customers: int = 200, months: int = 8) -> pd.DataFrame:
    rng = np.random.default_rng(0)
    rows = [
        {"Customer_ID": f"C{c}", "month_idx": m, "x": rng.random(), "Credit_Score": rng.integers(0, 3)}
        for c in range(n_customers)
        for m in range(months)
    ]
    return pd.DataFrame(rows)


def test_split_never_shares_a_customer_between_train_and_test():
    df = _panel()
    train, test = split_by_customer(df, test_size=0.2, seed=1)
    assert set(train.Customer_ID).isdisjoint(test.Customer_ID)
    assert len(train) + len(test) == len(df)


def test_split_keeps_all_months_of_each_customer_together():
    train, test = split_by_customer(_panel(), test_size=0.2, seed=1)
    assert (train.groupby("Customer_ID").size() == 8).all()
    assert (test.groupby("Customer_ID").size() == 8).all()


def test_assert_disjoint_raises_on_overlap():
    df = _panel(10)
    with pytest.raises(AssertionError):
        assert_disjoint_customers(df.iloc[:20], df.iloc[10:30])


def test_group_cv_folds_do_not_share_customers():
    df = _panel()
    cv = group_cv(n_splits=5, seed=3)
    for train_idx, valid_idx in cv.split(df, df["Credit_Score"], groups=df["Customer_ID"]):
        assert set(df.iloc[train_idx].Customer_ID).isdisjoint(df.iloc[valid_idx].Customer_ID)
