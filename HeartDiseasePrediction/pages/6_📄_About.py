import streamlit as st

st.title("📄 About")

st.write("""
This project is a professional Streamlit-based application for heart disease risk prediction.
It uses a structured dataset and machine learning models to train and evaluate predictive systems for cardiovascular health.
""")

st.subheader("Dataset")
st.write("The dataset contains patient attributes such as age, gender, chest pain type, resting blood pressure, cholesterol, fasting blood sugar, ECG results, maximum heart rate, exercise angina, oldpeak, ST slope, and the target label.")

st.subheader("Technologies")
st.write("- Python\n- Streamlit\n- Pandas\n- Scikit-learn\n- Plotly\n- ReportLab")

st.subheader("Workflow")
st.write("1. Load and analyze the dataset\n2. Train multiple machine learning models\n3. Compare performance metrics\n4. Save the best model\n5. Predict heart disease risk for new patients")

st.subheader("Developer")
st.write("Built as an AI/ML portfolio project with a modern medical-themed interface.")
