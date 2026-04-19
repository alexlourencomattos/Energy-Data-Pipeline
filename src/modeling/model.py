import os
from pathlib import Path
from typing import Tuple

import pandas as pd

SILVER_FILE = Path(os.getenv("SILVER_FILE", "data/silver/ena_clean.parquet"))
GOLD_DIR = Path(os.getenv("GOLD_DIR", "data/gold"))


def create_dimensions(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    dim_time = df[["date"]].drop_duplicates().copy()
    dim_time["year"] = dim_time["date"].dt.year
    dim_time["month"] = dim_time["date"].dt.month
    dim_time["day"] = dim_time["date"].dt.day

    dim_subsystem = df[["subsystem"]].drop_duplicates().copy()
    return dim_time, dim_subsystem


def create_fact(df: pd.DataFrame) -> pd.DataFrame:
    return df[["date", "subsystem", "ena_mwmed"]].copy()


def save_gold(dim_time: pd.DataFrame, dim_subsystem: pd.DataFrame, fact: pd.DataFrame) -> None:
    GOLD_DIR.mkdir(parents=True, exist_ok=True)
    dim_time.to_parquet(GOLD_DIR / "dim_time.parquet", index=False)
    dim_subsystem.to_parquet(GOLD_DIR / "dim_subsystem.parquet", index=False)
    fact.to_parquet(GOLD_DIR / "fact_ena.parquet", index=False)


def run_modeling() -> None:
    df = pd.read_parquet(SILVER_FILE)
    dim_time, dim_subsystem = create_dimensions(df)
    fact = create_fact(df)
    save_gold(dim_time, dim_subsystem, fact)
