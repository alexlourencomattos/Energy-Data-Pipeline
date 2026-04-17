import pandas as pd
import requests
import os
import logging
from datetime import datetime
from io import BytesIO

# Logging
logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def download_file(url: str) -> BytesIO:
    try:
        logging.info(f"Downloading file from {url}")
        response = requests.get(url)
        response.raise_for_status()

        logging.info("Download successful")
        return BytesIO(response.content)

    except Exception as e:
        logging.error(f"Download error: {e}")
        raise


def read_excel(file_bytes: BytesIO) -> pd.DataFrame:
    try:
        logging.info("Reading Excel file")

        df = pd.read_excel(file_bytes)

        logging.info(f"Excel loaded with {len(df)} rows")
        return df

    except Exception as e:
        logging.error(f"Error reading Excel: {e}")
        raise


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    try:
        logging.info("Starting transformation")

        # Padronizar nomes das colunas
        df.columns = [col.strip().lower() for col in df.columns]

        # Exemplo: renomear colunas comuns
        rename_map = {
            "nom_subsistema": "subsystem",
            "ena_bruta_regiao_mwmed": "ena_mwmed",
            "ena_data": "date"
        }

        df = df.rename(columns=rename_map)

        # Converter datas
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])

        logging.info("Transformation completed")
        return df

    except Exception as e:
        logging.error(f"Transformation error: {e}")
        raise


def validate_schema(df: pd.DataFrame):
    required_columns = ["date", "subsystem", "ena_mwmed"]

    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

def save_partitioned_parquet(df: pd.DataFrame, base_path: str):
    try:
        logging.info("Starting partitioned save")

        # Garantir que tem coluna de data
        if "date" not in df.columns:
            raise ValueError("Column 'date' is required for partitioning")

        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.month
        df["day"] = df["date"].dt.day

        for (year, month, day), group in df.groupby(["year", "month", "day"]):
            path = f"{base_path}/year={year}/month={month}/day={day}/data.parquet"
            os.makedirs(os.path.dirname(path), exist_ok=True)

            group.drop(columns=["year", "month", "day"]).to_parquet(path, index=False)

        logging.info("Partitioned save completed")

    except Exception as e:
        logging.error(f"Partitioned save error: {e}")
        raise


def run_ingestion():

        url = "https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/ena_subsistema_di/ENA_DIARIO_SUBSISTEMA_2026.xlsx"

        file_bytes = download_file(url)
        df_raw = read_excel(file_bytes)
        df_clean = transform_data(df_raw)
        validate_schema(df_clean)

        save_partitioned_parquet(df_clean, "data/bronze/ena")

        logging.info("Ingestion completed successfully")