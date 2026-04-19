import pandas as pd
import pytest

from src.ingestion.dataextract import transform_data, validate_schema


def test_transform_data_standardizes_columns():
    df = pd.DataFrame(
        {
            "nom_subsistema": ["SE"],
            "ena_bruta_regiao_mwmed": [123.4],
            "ena_data": ["2026-01-01"],
        }
    )

    result = transform_data(df)

    assert set(["subsystem", "ena_mwmed", "date"]).issubset(result.columns)


def test_validate_schema_raises_on_missing_columns():
    df = pd.DataFrame({"date": ["2026-01-01"], "subsystem": ["SE"]})

    with pytest.raises(ValueError):
        validate_schema(df)
