import os
from pathlib import Path

import duckdb
import pandas as pd
import plotly.express as px
import streamlit as st

FACT_FILE = Path(os.getenv("FACT_FILE", "data/gold/fact_ena.parquet"))

st.set_page_config(page_title="Energy Data Dashboard", layout="wide")
st.title("⚡ Energy Data Analytics – ENA")

if not FACT_FILE.exists():
    st.error(
        "Arquivo fact_ena.parquet não encontrado. Rode o pipeline antes de abrir o dashboard."
    )
    st.stop()

con = duckdb.connect()
df = con.execute(f"SELECT * FROM '{FACT_FILE}'").df()
df["date"] = pd.to_datetime(df["date"])

st.sidebar.header("Filtros")
subsystems = st.sidebar.multiselect(
    "Selecione subsistema",
    options=df["subsystem"].unique(),
    default=df["subsystem"].unique(),
)

filtered = df[df["subsystem"].isin(subsystems)].copy()

st.subheader("📈 ENA ao longo do tempo")
fig1 = px.line(
    filtered,
    x="date",
    y="ena_mwmed",
    color="subsystem",
    title="ENA por subsistema",
)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("📊 Média ENA por subsistema")
df_avg = filtered.groupby("subsystem", as_index=False)["ena_mwmed"].mean()
fig2 = px.bar(df_avg, x="subsystem", y="ena_mwmed", title="Média ENA")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("📅 Tendência mensal")
filtered["year_month"] = filtered["date"].dt.to_period("M").astype(str)
df_month = filtered.groupby(["year_month", "subsystem"], as_index=False)["ena_mwmed"].mean()
fig3 = px.line(
    df_month,
    x="year_month",
    y="ena_mwmed",
    color="subsystem",
    title="Tendência mensal de ENA",
)
st.plotly_chart(fig3, use_container_width=True)
