import streamlit as st, pandas as pd

st.set_page_config(page_title="Fraud & Compliance Analytics", layout="wide")
st.title("🕵️ Real-Time Fraud & Compliance (Demo)")

enriched = pd.read_csv("data/processed/transactions_enriched.csv")
k_country = pd.read_csv("data/processed/kpi_by_country.csv")
k_channel = pd.read_csv("data/processed/kpi_by_channel.csv")

c1, c2 = st.columns(2)
with c1:
    st.subheader("Flag Rate by Country")
    st.bar_chart(k_country.set_index("country")["flag_rate"])
with c2:
    st.subheader("Flag Rate by Channel")
    st.bar_chart(k_channel.set_index("channel")["flag_rate"])

st.subheader("Sample Events")
st.dataframe(enriched.head(10), use_container_width=True)
st.caption("Demo pipeline. Replace ingest with Kafka and processing with Spark/Databricks later.")
