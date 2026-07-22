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

with st.expander("Column Descriptions"):
    st.markdown(
        """
        **Let's understand our columns better:**

        - **Age:** Patient's age in years
        - **Sex:** M = Male, F = Female
        - **ChestPainType:** Type of chest pain
          - TA = Typical Angina
          - ATA = Atypical Angina
          - NAP = Non-Anginal Pain
          - ASY = Asymptomatic
        - **RestingBP:** Resting blood pressure (mm Hg)
        - **Cholesterol:** Serum cholesterol level in mg/dL
        - **FastingBS:** Fasting blood sugar
          - 1 = Blood sugar > 120 mg/dL
          - 0 = Blood sugar ≤ 120 mg/dL
        - **RestingECG:** Resting electrocardiographic results
          - Normal = Normal ECG
          - ST = ST-T wave abnormality
          - LVH = Left Ventricular Hypertrophy
        - **MaxHR:** Maximum heart rate achieved during exercise
        - **ExerciseAngina:** Exercise-induced angina
          - Y = Yes
          - N = No
        - **Oldpeak:** ST depression induced by exercise relative to rest
        - **ST_Slope:** Slope of the peak exercise ST segment
          - Up = Upsloping
          - Flat = Flat
          - Down = Downsloping
        - **HeartDisease:** Target variable
          - 1 = Heart Disease
          - 0 = No Heart Disease
        """,
        unsafe_allow_html=True,
    )

with st.expander("Data Types"):
    st.dataframe(df.dtypes.reset_index().rename(columns={"index": "Column", 0: "Type"}), use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(plot_heart_disease_distribution(df), use_container_width=True)
with col2:
    st.plotly_chart(plot_gender_distribution(df), use_container_width=True)

st.plotly_chart(plot_age_distribution(df), use_container_width=True)
