import os
from pathlib import Path

import duckdb

GOLD_DIR = Path(os.getenv("GOLD_DIR", "data/gold"))
ANALYTICS_DIR = Path(os.getenv("ANALYTICS_DIR", "data/analytics"))


def run_queries() -> None:
    ANALYTICS_DIR.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect()
    con.execute(
        f"""
        CREATE VIEW fact_ena AS
        SELECT * FROM '{GOLD_DIR / 'fact_ena.parquet'}'
    """
    )

    con.execute(
        f"""
        CREATE VIEW dim_time AS
        SELECT * FROM '{GOLD_DIR / 'dim_time.parquet'}'
    """
    )

    con.execute(
        f"""
        CREATE VIEW dim_subsystem AS
        SELECT * FROM '{GOLD_DIR / 'dim_subsystem.parquet'}'
    """
    )

    result1 = con.execute(
        """
        SELECT
            subsystem,
            AVG(ena_mwmed) AS avg_ena
        FROM fact_ena
        GROUP BY subsystem
        ORDER BY avg_ena DESC
    """
    ).df()
    result1.to_parquet(ANALYTICS_DIR / "avg_ena.parquet")

    result2 = con.execute(
        """
        SELECT
            t.year,
            t.month,
            AVG(f.ena_mwmed) AS avg_ena
        FROM fact_ena f
        JOIN dim_time t ON f.date = t.date
        GROUP BY t.year, t.month
        ORDER BY t.year, t.month
    """
    ).df()

    result3 = con.execute(
        """
        SELECT
            date,
            subsystem,
            ena_mwmed,
            RANK() OVER (PARTITION BY date ORDER BY ena_mwmed DESC) AS rank
        FROM fact_ena
    """
    ).df()

    print("\nENA Submarket Average:")
    print(result1)
    print("\nENA Month Average:")
    print(result2)
    print("\nDaily Ranking:")
    print(result3.head())
