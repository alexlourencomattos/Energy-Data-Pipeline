import pandas as pd
import os


def create_dimensions(df: pd.DataFrame):
    dim_time = df[["date"]].drop_duplicates()
    dim_time["year"] = dim_time["date"].dt.year
    dim_time["month"] = dim_time["date"].dt.month
    dim_time["day"] = dim_time["date"].dt.day

    dim_subsystem = df[["subsystem"]].drop_duplicates()

    return dim_time, dim_subsystem


def create_fact(df: pd.DataFrame):
    return df[["date", "subsystem", "ena_mwmed"]]


def save_gold(dim_time, dim_subsystem, fact):
    os.makedirs("data/gold", exist_ok=True)

    dim_time.to_parquet("data/gold/dim_time.parquet", index=False)
    dim_subsystem.to_parquet("data/gold/dim_subsystem.parquet", index=False)
    fact.to_parquet("data/gold/fact_ena.parquet", index=False)


def run_modeling():
    df = pd.read_parquet("data/silver/ena_clean.parquet")

    dim_time, dim_subsystem = create_dimensions(df)
    fact = create_fact(df)

    save_gold(dim_time, dim_subsystem, fact)