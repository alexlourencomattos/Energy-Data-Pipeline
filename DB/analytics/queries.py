import duckdb


def run_queries():
    con = duckdb.connect()

    # Registrar tabelas Parquet
    con.execute("""
        CREATE VIEW fact_ena AS 
        SELECT * FROM 'data/gold/fact_ena.parquet'
    """)

    con.execute("""
        CREATE VIEW dim_time AS 
        SELECT * FROM 'data/gold/dim_time.parquet'
    """)

    con.execute("""
        CREATE VIEW dim_subsystem AS 
        SELECT * FROM 'data/gold/dim_subsystem.parquet'
    """)

    # Query 1: ENA Subsystem Average
    result1 = con.execute("""
        SELECT 
            subsystem,
            AVG(ena_mwmed) AS avg_ena
        FROM fact_ena
        GROUP BY subsystem
        ORDER BY avg_ena DESC
    """).df()

    result1.to_parquet("data/analytics/avg_ena.parquet")
    print("\nENA Submarket Average:")
    print(result1)

    # Query 2: Monthly
    result2 = con.execute("""
        SELECT 
            t.year,
            t.month,
            AVG(f.ena_mwmed) AS avg_ena
        FROM fact_ena f
        JOIN dim_time t ON f.date = t.date
        GROUP BY t.year, t.month
        ORDER BY t.year, t.month
    """).df()

    print("\nENA Month Average:")
    print(result2)

    # Query 3:  Daily Subsystem Ranking
    result3 = con.execute("""
        SELECT 
            date,
            subsystem,
            ena_mwmed,
            RANK() OVER (PARTITION BY date ORDER BY ena_mwmed DESC) AS rank
        FROM fact_ena
    """).df()

    print("\nDaily Ranking:")
    print(result3.head())