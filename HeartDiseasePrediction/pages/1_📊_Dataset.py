import pandas as pd
import streamlit as st

from utils.preprocessing import load_dataset
from utils.visualization import plot_age_distribution, plot_gender_distribution, plot_heart_disease_distribution

st.set_page_config(page_title="Dataset", page_icon="📊", layout="wide")

st.title("📊 Dataset Overview")

df = load_dataset()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Rows", df.shape[0])
with col2:
    st.metric("Columns", df.shape[1])
with col3:
    st.metric("Missing Values", int(df.isna().sum().sum()))
with col4:
    st.metric("Duplicates", int(df.duplicated().sum()))

st.subheader("Dataset Preview")
st.dataframe(df.head(10), use_container_width=True)

with st.expander("Dataset Summary"):
    st.dataframe(df.describe(include="all"), use_container_width=True)

with st.expander("Data Types"):
    st.dataframe(df.dtypes.reset_index().rename(columns={"index": "Column", 0: "Type"}), use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(plot_heart_disease_distribution(df), use_container_width=True)
with col2:
    st.plotly_chart(plot_gender_distribution(df), use_container_width=True)

st.plotly_chart(plot_age_distribution(df), use_container_width=True)
