import logging
import os
from datetime import datetime
from io import BytesIO
from pathlib import Path

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

LOG_FILE = Path(os.getenv("LOG_FILE", "logs/pipeline.log"))
BRONZE_DIR = Path(os.getenv("BRONZE_DIR", "data/bronze/ena"))
INGESTION_YEAR = os.getenv("INGESTION_YEAR", str(datetime.utcnow().year))
INGESTION_URL = os.getenv(
    "INGESTION_URL",
    f"https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/ena_subsistema_di/"
    f"ENA_DIARIO_SUBSISTEMA_{INGESTION_YEAR}.xlsx",
)

LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def _build_session() -> requests.Session:
    retry = Retry(total=3, backoff_factor=0.8, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)

    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def download_file(url: str, timeout: int = 30) -> BytesIO:
    try:
        logging.info("Downloading file from %s", url)
        with _build_session() as session:
            response = session.get(url, timeout=timeout)
            response.raise_for_status()

        logging.info("Download successful")
        return BytesIO(response.content)
    except Exception as exc:
        logging.error("Download error: %s", exc)
        raise


def read_excel(file_bytes: BytesIO) -> pd.DataFrame:
    try:
        logging.info("Reading Excel file")
        df = pd.read_excel(file_bytes)
        logging.info("Excel loaded with %s rows", len(df))
        return df
    except Exception as exc:
        logging.error("Error reading Excel: %s", exc)
        raise


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    try:
        logging.info("Starting transformation")
        df = df.copy()
        df.columns = [col.strip().lower() for col in df.columns]

        rename_map = {
            "nom_subsistema": "subsystem",
            "ena_bruta_regiao_mwmed": "ena_mwmed",
            "ena_data": "date",
        }
        df = df.rename(columns=rename_map)

        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")

        logging.info("Transformation completed")
        return df
    except Exception as exc:
        logging.error("Transformation error: %s", exc)
        raise


def validate_schema(df: pd.DataFrame) -> None:
    required_columns = ["date", "subsystem", "ena_mwmed"]
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required column(s): {', '.join(missing_columns)}")


def save_partitioned_parquet(df: pd.DataFrame, base_path: Path) -> None:
    try:
        logging.info("Starting partitioned save")
        if "date" not in df.columns:
            raise ValueError("Column 'date' is required for partitioning")

        data = df.copy()
        data["year"] = data["date"].dt.year
        data["month"] = data["date"].dt.month
        data["day"] = data["date"].dt.day

        for (year, month, day), group in data.groupby(["year", "month", "day"]):
            path = base_path / f"year={year}" / f"month={month}" / f"day={day}" / "data.parquet"
            path.parent.mkdir(parents=True, exist_ok=True)
            group.drop(columns=["year", "month", "day"]).to_parquet(path, index=False)

        logging.info("Partitioned save completed")
    except Exception as exc:
        logging.error("Partitioned save error: %s", exc)
        raise


def run_ingestion() -> None:
    file_bytes = download_file(INGESTION_URL)
    df_raw = read_excel(file_bytes)
    df_clean = transform_data(df_raw)
    validate_schema(df_clean)
    save_partitioned_parquet(df_clean, BRONZE_DIR)
    logging.info("Ingestion completed successfully")
