import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Energy Data Dashboard", layout="wide")

st.title("⚡ Energy Data Analytics – ENA")

# conexão com DuckDB
con = duckdb.connect()

# carregar dados
df = con.execute("""
    SELECT * FROM 'data/gold/fact_ena.parquet'
""").df()

df["date"] = pd.to_datetime(df["date"])

# filtros
st.sidebar.header("Filters")

subsystems = st.sidebar.multiselect(
    "Select subsystem",
    options=df["subsystem"].unique(),
    default=df["subsystem"].unique()
)

df = df[df["subsystem"].isin(subsystems)]

# gráfico 1: série temporal
st.subheader("📈 ENA Over Time")

fig1 = px.line(
    df,
    x="date",
    y="ena_mwmed",
    color="subsystem",
    title="ENA by Subsystem"
)

st.plotly_chart(fig1, use_container_width=True)

# gráfico 2: média por subsistema
st.subheader("📊 Average ENA by Subsystem")

df_avg = df.groupby("subsystem")["ena_mwmed"].mean().reset_index()

fig2 = px.bar(
    df_avg,
    x="subsystem",
    y="ena_mwmed",
    title="Average ENA"
)

st.plotly_chart(fig2, use_container_width=True)

# gráfico 3: agregação mensal
st.subheader("📅 Monthly Trend")

df["year_month"] = df["date"].dt.to_period("M").astype(str)

df_month = df.groupby(["year_month", "subsystem"])["ena_mwmed"].mean().reset_index()

fig3 = px.line(
    df_month,
    x="year_month",
    y="ena_mwmed",
    color="subsystem",
    title="Monthly ENA Trend"
)

st.plotly_chart(fig3, use_container_width=True)