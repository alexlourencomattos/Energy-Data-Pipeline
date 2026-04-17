# ⚡ Energy Data Platform – End-to-End Data Engineering Project

This project demonstrates a production-oriented data platform 
designed to ingest, process, model, and analyze large-scale 
energy data using modern data engineering practices.

It showcases how raw data can be transformed into reliable, 
analytics-ready datasets and business insights, 
following industry standards used in data-driven organizations.

## 🎯 Objective

Build a complete end-to-end data pipeline that:

- Ingests real-world data from the ONS
- Applies structured transformations and data validation
- Organizes data using a Data Lake (Medallion Architecture)
- Models data for analytical consumption (Star Schema)
- Enables querying and visualization for decision-making

## 🧱 Architecture Overview

``` mermaid
flowchart LR

A[Data Sources] --> B[Ingestion Layer]
B --> C[Raw Data - Bronze]
C --> D[Processed Data - Silver]
D --> E[Curated Data - Gold]
E --> F[Analytics / Dashboard]

D --> M[Hydrology Model - R]
M --> E

L[Logging] --- B
T[Tests] --- D
O[Airflow] -.-> B

```
## 🔄 Data Engineering Workflow

### 1. Data Ingestion (ETL)
Source: ONS Open Data (Excel via HTTP)
Technology: Python (Pandas)
Output: Parquet files (Bronze layer)

### 2. Data Storage (Data Lake)
Format: Parquet
Architecture:
Bronze → Raw data (partitioned by date)
Silver → Cleaned and validated data
Gold → Curated analytical datasets

### 3. Data Transformation (Silver Layer)
Data cleaning and normalization
Type enforcement and validation
Handling missing and invalid values

### 4. Data Modeling (Gold Layer)

Star Schema:
fact_ena → energy metrics
dim_time → temporal attributes
dim_subsystem → system segmentation

### 5. Analytics (SQL Layer)

Technology: DuckDB
Queries:
Aggregations (AVG, GROUP BY)
Joins (fact + dimensions)
Window functions (ranking)

### 6. Data Visualization
Technology: Streamlit + Plotly
Features:
Time-series analysis
Subsystem comparison
Monthly trends

## ⚙️ Tech Stack
- Python (Pandas, DuckDB)
- SQL (analytical queries)
- Parquet (Data Lake storage)
- Apache Airflow (orchestration)
- Docker / Kubernetes (conceptual)
- Streamlit + Plotly (dashboard)
- Pytest (unit testing)

## 🛠️ Engineering Best Practices

✔️ Data Lake Partitioning
- Partitioned by year/month/day
- Improves performance and scalability

✔️ Logging
- Structured logs for pipeline execution
- Error tracking and traceability

✔️ Unit Testing
- Validates transformations and modeling
- Ensures reliability and safe refactoring

✔️ Orchestration
- Airflow DAG controlling pipeline execution
- Task dependencies and retry logic

## ▶️ How to Run
1. Install dependencies
```bash
pip install pandas requests pyarrow openpyxl duckdb streamlit plotly pytest
```
2. Run the pipeline
``` bash
python main.py
```

3. Run tests
```bash
pytest
```
4. Launch dashboard
```bash
streamlit run src/dashboard/app.py
```

## 📊 Example Use Cases
- Monitor energy inflows (ENA) over time
- Compare subsystem performance
- Analyze seasonal patterns
- Support data-driven decision-making

## 🎯 Key Highlights
- End-to-end pipeline (ingestion → analytics)
- Data Lake with Medallion Architecture
- Star Schema modeling
- SQL-based analytics
- Orchestration with Airflow
- Data quality and testing
- Interactive dashboard

## 🚀 Why This Project

- Build scalable data pipelines
- Design analytical data models
- Ensure data reliability and quality
- Deliver data products for business use