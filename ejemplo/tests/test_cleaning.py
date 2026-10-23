import numpy as np
import pandas as pd

from creditsight.data.cleaning import _to_number, clean, parse_credit_history


def _frame(**overrides) -> pd.DataFrame:
    """Un cliente con 3 meses; cada prueba sobrescribe lo que necesita."""
    base = {
        "Customer_ID": ["C1"] * 3,
        "Month": ["January", "February", "March"],
        "Age": ["23", "23_", "-500"],
        "Occupation": ["Scientist", "_______", "Scientist"],
        "Annual_Income": ["19114.12", "19114.12_", "24198062"],
        "Num_Bank_Accounts": [3, 3, 1798],
        "Num_Credit_Card": [4, 4, 4],
        "Monthly_Inhand_Salary": [1000.0, np.nan, 1000.0],
        "Interest_Rate": [3, 3, 5797],
        "Num_of_Loan": ["4", "4_", "-100"],
        "Num_of_Delayed_Payment": ["7", "_", "7_"],
        "Changed_Credit_Limit": ["11.27", "_", "5.0"],
        "Outstanding_Debt": ["809.98", "809.98_", "809.98"],
        "Amount_invested_monthly": ["80.4", "__10000__", "50.0"],
        "Monthly_Balance": ["312.0", "__-333333333333333333333333333__", "300.0"],
        "Num_Credit_Inquiries": [4.0, 4.0, 2597.0],
        "Total_EMI_per_month": [49.5, 49.5, 82331.0],
        "Credit_History_Age": ["22 Years and 1 Months", None, "22 Years and 3 Months"],
        "Credit_Mix": ["_", "Good", "Good"],
        "Payment_Behaviour": ["!@9#%8", "Low_spent_Small_value_payments", "Low_spent_Small_value_payments"],
    }
    base.update(overrides)
    return pd.DataFrame(base)


def test_to_number_strips_trailing_underscore_and_coerces_garbage():
    result = _to_number(pd.Series(["23_", "40", "_", "abc"]))
    assert result.iloc[0] == 23 and result.iloc[1] == 40
    assert result.iloc[2:].isna().all()


def test_clean_keeps_rows_and_removes_pii():
    out = clean(_frame())
    assert len(out) == 3
    for col in ["Name", "SSN", "ID"]:
        assert col not in out.columns


def test_clean_marks_sentinels_and_implausible_values_as_missing():
    out = clean(_frame())
    assert out["Amount_invested_monthly"].isna().tolist() == [False, True, False]
    assert out["Monthly_Balance"].isna().tolist() == [False, True, False]
    assert out["Changed_Credit_Limit"].isna().tolist() == [False, True, False]
    assert out["Num_Credit_Inquiries"].isna().tolist() == [False, False, True]
    assert out["Total_EMI_per_month"].isna().tolist() == [False, False, True]


def test_stable_columns_are_repaired_with_the_customers_valid_mode():
    out = clean(_frame())
    assert out["Age"].tolist() == [23, 23, 23]
    assert out["Occupation"].tolist() == ["Scientist"] * 3
    assert out["Annual_Income"].nunique() == 1
    assert out["Num_Bank_Accounts"].tolist() == [3, 3, 3]
    assert out["Interest_Rate"].tolist() == [3, 3, 3]
    assert out["Num_of_Loan"].tolist() == [4, 4, 4]


def test_credit_mix_and_salary_are_repaired_per_customer():
    out = clean(_frame())
    assert out["Credit_Mix"].tolist() == ["Good"] * 3  # "_" en enero se repara con el valor del cliente
    assert out["Monthly_Inhand_Salary"].tolist() == [1000.0] * 3


def test_payment_behaviour_garbage_stays_missing():
    out = clean(_frame())
    assert out["Payment_Behaviour"].isna().tolist() == [True, False, False]


def test_credit_history_is_reconstructed_one_month_per_month():
    out = clean(_frame())
    # 22 años y 1 mes = 265 meses en enero; el mes siguiente debe ser 266 aunque venga vacío
    assert out["Credit_History_Months"].tolist() == [265, 266, 267]


def test_parse_credit_history_handles_missing():
    parsed = parse_credit_history(pd.Series(["22 Years and 1 Months", np.nan]))
    assert parsed.iloc[0] == 265 and np.isnan(parsed.iloc[1])
