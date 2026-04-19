import glob
import logging
import os
from pathlib import Path

import pandas as pd

BRONZE_DIR = Path(os.getenv("BRONZE_DIR", "data/bronze/ena"))
SILVER_DIR = Path(os.getenv("SILVER_DIR", "data/silver"))


def read_bronze_data(path: Path) -> pd.DataFrame:
    files = glob.glob(f"{path}/**/*.parquet", recursive=True)
    if not files:
        raise FileNotFoundError(f"No parquet files found in bronze path: {path}")

    df_list = [pd.read_parquet(file_path) for file_path in files]
    return pd.concat(df_list, ignore_index=True)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Cleaning data")
    cleaned = df.dropna(subset=["date", "subsystem", "ena_mwmed"]).copy()
    cleaned["ena_mwmed"] = pd.to_numeric(cleaned["ena_mwmed"], errors="coerce")
    cleaned = cleaned.dropna(subset=["ena_mwmed"])
    cleaned = cleaned[cleaned["ena_mwmed"] >= 0]
    return cleaned


def save_silver(df: pd.DataFrame, path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path / "ena_clean.parquet", index=False)


def run_silver() -> None:
    df = read_bronze_data(BRONZE_DIR)
    df_clean = clean_data(df)
    save_silver(df_clean, SILVER_DIR)
    logging.info("Silver layer completed")
