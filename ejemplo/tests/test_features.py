import numpy as np
import pandas as pd

from creditsight.features.engineering import LOAN_TYPES, add_features, build_preprocessor, feature_columns


def _row(**kw) -> pd.DataFrame:
    base = {
        "Outstanding_Debt": [1000.0], "Annual_Income": [50000.0], "Total_EMI_per_month": [100.0],
        "Monthly_Inhand_Salary": [4000.0], "Amount_invested_monthly": [200.0], "Monthly_Balance": [400.0],
        "Type_of_Loan": ["Auto Loan, Student Loan, and Personal Loan"],
    }
    base.update(kw)
    return pd.DataFrame(base)


def test_ratios_and_loan_flags():
    out = add_features(_row())
    assert out["debt_to_income"].iloc[0] == 1000 / 50000
    assert out["emi_to_salary"].iloc[0] == 100 / 4000
    assert out["n_loan_types"].iloc[0] == 3
    assert out[f"loan_{LOAN_TYPES.index('Auto Loan')}"].iloc[0] == 1.0


def test_division_by_zero_or_missing_gives_nan_not_inf():
    out = add_features(_row(Annual_Income=[0.0], Monthly_Inhand_Salary=[np.nan]))
    assert np.isnan(out["debt_to_income"].iloc[0]) and np.isnan(out["emi_to_salary"].iloc[0])
    assert not np.isinf(out.select_dtypes("number").to_numpy(dtype=float)).any()


def test_no_loans_means_zero_flags():
    out = add_features(_row(Type_of_Loan=[np.nan]))
    assert out["n_loan_types"].iloc[0] == 0


def test_add_features_does_not_mutate_input():
    frame = _row()
    add_features(frame)
    assert "debt_to_income" not in frame.columns


def test_feature_columns_toggles():
    num_all, cat_all = feature_columns(use_credit_mix=True, use_engineered=True)
    num_min, cat_min = feature_columns(use_credit_mix=False, use_engineered=False, extra_numeric=["x"])
    assert "Credit_Mix" in cat_all and "Credit_Mix" not in cat_min
    assert "debt_to_income" in num_all and "debt_to_income" not in num_min and "x" in num_min


def test_preprocessor_handles_unseen_category_and_missing():
    num, cat = feature_columns(use_credit_mix=True)
    train = pd.DataFrame({c: [1.0, 2.0, np.nan, 4.0] for c in num})
    for c in cat:
        train[c] = ["a", "b", "a", np.nan]
    prep = build_preprocessor(use_credit_mix=True).fit(train)
    new = train.iloc[:2].copy()
    for c in cat:
        new[c] = ["nunca_visto", np.nan]
    assert not np.isnan(prep.transform(new)).any()
