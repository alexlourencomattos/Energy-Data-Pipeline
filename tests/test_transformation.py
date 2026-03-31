import pandas as pd
from src.transformation.silver import clean_data


def test_clean_data_removes_nulls():
    df = pd.DataFrame({
        "date": ["2026-01-01", None],
        "subsystem": ["SE", "S"],
        "ena_mwmed": [100, 200]
    })

    df["date"] = pd.to_datetime(df["date"])

    result = clean_data(df)

    assert len(result) == 1


def test_clean_data_removes_negative_values():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2026-01-01", "2026-01-02"]),
        "subsystem": ["SE", "S"],
        "ena_mwmed": [100, -50]
    })

    result = clean_data(df)

    assert (result["ena_mwmed"] >= 0).all()