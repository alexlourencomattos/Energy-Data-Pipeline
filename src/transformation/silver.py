import pandas as pd
import glob
import logging
import os

def read_bronze_data(path: str) -> pd.DataFrame:
    files = glob.glob(f"{path}/**/*.parquet", recursive=True)
    df_list = [pd.read_parquet(f) for f in files]

    return pd.concat(df_list, ignore_index=True)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Cleaning data")

    # remover nulos críticos
    df = df.dropna(subset=["date", "subsystem", "ena_mwmed"])

    # garantir tipos
    df["ena_mwmed"] = pd.to_numeric(df["ena_mwmed"], errors="coerce")

    # remover valores inválidos
    df = df[df["ena_mwmed"] >= 0]

    return df


def save_silver(df: pd.DataFrame, path: str):
    os.makedirs(path, exist_ok=True)
    df.to_parquet(f"{path}/ena_clean.parquet", index=False)


def run_silver():
    df = read_bronze_data("data/bronze/ena")
    df_clean = clean_data(df)
    save_silver(df_clean, "data/silver")

    logging.info("Silver layer completed")