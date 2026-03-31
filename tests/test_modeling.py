import pandas as pd
from src.modeling.model import create_fact, create_dimensions


def test_create_fact():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2026-01-01"]),
        "subsystem": ["SE"],
        "ena_mwmed": [100]
    })

    fact = create_fact(df)

    assert list(fact.columns) == ["date", "subsystem", "ena_mwmed"]


def test_create_dimensions():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2026-01-01"]),
        "subsystem": ["SE"],
        "ena_mwmed": [100]
    })

    dim_time, dim_subsystem = create_dimensions(df)

    assert "year" in dim_time.columns
    assert len(dim_subsystem) == 1

def test_required_columns():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2026-01-01"]),
        "subsystem": ["SE"],
        "ena_mwmed": [100]
    })

    assert all(col in df.columns for col in ["date", "subsystem", "ena_mwmed"])