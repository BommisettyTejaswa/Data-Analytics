import streamlit as st

from utils.preprocessing import load_dataset
from utils.visualization import (
    plot_boxplot,
    plot_chest_pain_analysis,
    plot_cholesterol_distribution,
    plot_correlation_heatmap,
    plot_histogram,
    plot_max_hr_distribution,
)

st.title("📈 Exploratory Data Analysis")

df = load_dataset()

selected_column = st.selectbox("Choose a feature", [
    "Age",
    "RestingBP",
    "Cholesterol",
    "MaxHR",
    "Oldpeak",
])

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(plot_boxplot(df, selected_column), use_container_width=True)
with col2:
    st.plotly_chart(plot_histogram(df, selected_column), use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(plot_chest_pain_analysis(df), use_container_width=True)
with col2:
    st.plotly_chart(plot_cholesterol_distribution(df), use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(plot_max_hr_distribution(df), use_container_width=True)
with col2:
    st.plotly_chart(plot_correlation_heatmap(df), use_container_width=True)
