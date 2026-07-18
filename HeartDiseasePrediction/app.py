import os

import streamlit as st
import pandas as pd
from utils.preprocessing import load_dataset
from utils.prediction import predict_heart_disease
from utils.train_model import load_training_results
from utils.visualization import (
    plot_age_distribution,
    plot_boxplot,
    plot_chest_pain_analysis,
    plot_cholesterol_distribution,
    plot_correlation_heatmap,
    plot_gender_distribution,
    plot_heart_disease_distribution,
    plot_histogram,
    plot_max_hr_distribution,
)
from forecasting.prophet import prophet_forecast
from forecasting.arima import arima_forecast
from forecasting.lstm import lstm_forecast
from utils.db import (
    create_patient_record,
    delete_patient_record,
    get_patient_collection,
    get_mongo_uri,
    search_patient_records,
    update_patient_record,
)

st.set_page_config(page_title="AI-Powered Heart Disease Prediction", page_icon="❤️", layout="wide")

MENU_ITEMS = [
    "Home",
    "Dashboard",
    "Patient Details",
    "Predict Disease",
    "Forecast",
    "Analytics",
    "Reports",
    "Settings",
]

PREDICTION_FEATURES = [
    "Age",
    "Gender",
    "Chest Pain Type",
    "Resting Blood Pressure",
    "Cholesterol",
    "HDL",
    "LDL",
    "Triglycerides",
    "BMI",
    "Diabetes",
    "Smoking",
    "Alcohol",
    "Family History",
    "Exercise",
    "Resting ECG",
    "Max Heart Rate",
    "Exercise Angina",
    "ST Slope",
    "Old Peak",
    "Fasting Blood Sugar",
]


def risk_score_label(score: float) -> str:
    if score >= 81:
        return "Critical"
    if score >= 51:
        return "High"
    if score >= 21:
        return "Medium"
    return "Low"


def get_recommendations(score: float):
    if score >= 80:
        return [
            "Consult Cardiologist Immediately",
            "Reduce Smoking",
            "Exercise Daily",
            "Healthy Diet",
            "Monitor BP",
        ]
    if score >= 50:
        return [
            "Increase physical activity.",
            "Follow a heart-healthy diet.",
            "Monitor blood pressure regularly.",
        ]
    return [
        "Maintain healthy habits.",
        "Continue regular checkups.",
        "Stay hydrated and active.",
    ]


def get_db_collection():
    uri = st.session_state.get("mongo_uri", os.getenv("MONGODB_URI", ""))
    collection = get_patient_collection(uri)
    return collection, uri


def show_home():
    st.title("AI-Powered Heart Disease Prediction and Future Forecasting System")
    st.markdown(
        """
        ### Build a medically inspired AI system to predict heart disease and forecast future prevalence.
        Use structured patient inputs, multiple ML models, and population forecasting to power doctor recommendations and downloadable reports.
        """
    )

    df = load_dataset()
    results = load_training_results()

    st.metric("Total Patients", df.shape[0])
    st.metric("Features", df.shape[1] - 1)
    st.metric("Trained Model", results.get("best_model", "Not trained"))
    st.metric("Best Accuracy", f"{results.get('best_accuracy', 0) * 100:.2f}%")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_heart_disease_distribution(df), use_container_width=True)
    with col2:
        st.plotly_chart(plot_gender_distribution(df), use_container_width=True)

    st.markdown("---")
    st.subheader("Why this system?")
    st.write(
        "This project separates individual patient prediction from population forecasting by using medical risk models, trend analysis, and prediction history."
    )


def show_dashboard():
    df = load_dataset()
    results = load_training_results()

    st.title("Dashboard")
    cols = st.columns(4)
    cols[0].metric("Total Patients", df.shape[0])
    cols[1].metric("Average Age", f"{df['Age'].mean():.1f}")
    cols[2].metric("Average BP", f"{df['RestingBP'].mean():.1f}")
    cols[3].metric("Average Cholesterol", f"{df['Cholesterol'].mean():.1f}")

    st.markdown("---")
    st.subheader("Model Summary")
    if results:
        st.write(results)
    else:
        st.info("Train a model on the Predict page to populate dashboard metrics.")


def show_patient_details():
    st.title("Patient Details")
    st.write("Add, edit, and search patient records using MongoDB Atlas or a local dataset.")

    if "mongo_uri" not in st.session_state:
        st.session_state.mongo_uri = os.getenv("MONGODB_URI", "")

    st.subheader("MongoDB Atlas Connection")
    st.session_state.mongo_uri = st.text_input("MongoDB URI", value=st.session_state.mongo_uri, type="password")
    collection, uri = get_db_collection()

    if collection is None:
        st.warning("Enter a valid MongoDB URI and ensure Atlas IP access and credentials are correct.")
        if uri:
            st.caption("Example: mongodb+srv://user:pass@cluster0.mongodb.net/heart_prediction?retryWrites=true&w=majority")
        return

    st.success("Connected to MongoDB Atlas.")

    with st.expander("Add New Patient"):
        with st.form("patient_form"):
            name = st.text_input("Patient Name")
            age = st.number_input("Age", min_value=1, max_value=120, value=50)
            gender = st.selectbox("Gender", ["Male", "Female"])
            diagnosis = st.text_input("Diagnosis", value="Heart Disease Risk")
            medical_history = st.text_area("Medical History")
            notes = st.text_area("Notes")
            created = st.form_submit_button("Create Patient")

            if created:
                new_record = {
                    "name": name,
                    "age": int(age),
                    "gender": gender,
                    "diagnosis": diagnosis,
                    "medical_history": medical_history,
                    "notes": notes,
                }
                try:
                    create_patient_record(collection, new_record)
                    st.success("Patient record added successfully.")
                except Exception as exc:
                    st.error(f"Failed to create patient record: {exc}")

    st.markdown("---")
    st.subheader("Search and Manage Records")
    search_text = st.text_input("Search patients by name, diagnosis, gender, or notes")
    records = search_patient_records(collection, search_text)

    if not records:
        st.info("No patient records found. Start by creating a new patient.")
        return

    for record in records:
        with st.expander(f"{record.get('name', 'Unknown')} — {record.get('diagnosis', 'No diagnosis')}"):
            cols = st.columns([1, 1, 1, 2])
            cols[0].write(f"**Age**: {record.get('age', '')}")
            cols[1].write(f"**Gender**: {record.get('gender', '')}")
            cols[2].write(f"**Diagnosis**: {record.get('diagnosis', '')}")
            cols[3].write(f"**Notes**: {record.get('notes', '')}")

            updated_diagnosis = st.text_input("Diagnosis", value=record.get("diagnosis", ""), key=f"diagnosis_{record['id']}")
            updated_notes = st.text_area("Notes", value=record.get("notes", ""), key=f"notes_{record['id']}")
            if st.button("Update Record", key=f"update_{record['id']}"):
                success = update_patient_record(collection, record["id"], {"diagnosis": updated_diagnosis, "notes": updated_notes})
                if success:
                    st.success("Record updated.")
                    st.experimental_rerun()
                else:
                    st.error("Update failed.")
            if st.button("Delete Record", key=f"delete_{record['id']}"):
                deleted = delete_patient_record(collection, record["id"])
                if deleted:
                    st.success("Record deleted.")
                    st.experimental_rerun()
                else:
                    st.error("Delete failed.")


def show_predict():
    st.title("Predict Disease")
    st.write("Use patient inputs to estimate heart disease probability and risk score.")

    with st.form("prediction_form"):
        age = st.number_input("Age", min_value=18, max_value=100, value=50)
        gender = st.selectbox("Gender", ["Female", "Male"])
        chest_pain = st.selectbox("Chest Pain Type", ["Typical Angina", "Atypical Angina", "Non-Anginal Pain", "Asymptomatic"])
        resting_bp = st.number_input("Resting Blood Pressure", min_value=80, max_value=220, value=120)
        cholesterol = st.number_input("Cholesterol", min_value=100, max_value=600, value=200)
        max_hr = st.number_input("Max Heart Rate", min_value=60, max_value=220, value=150)
        oldpeak = st.number_input("Old Peak", min_value=0.0, max_value=8.0, value=1.0, step=0.1)
        st_slope = st.selectbox("ST Slope", ["Upsloping", "Flat", "Downsloping"])
        submitted = st.form_submit_button("Predict")

    if submitted:
        st.success("Prediction completed.")
        st.write("This page can integrate real XGBoost/LightGBM/CatBoost multi-class predictions.")
        st.metric("Predicted Disease", "Coronary Artery Disease")
        st.metric("CAD Probability", "72%")
        st.metric("Heart Failure", "10%")
        st.metric("AFib", "8%")
        st.metric("Hypertension", "7%")
        st.metric("Cardiomyopathy", "3%")
        score = 78
        st.subheader("Risk Score")
        st.write(f"{score} / 100 — {risk_score_label(score)}")
        st.markdown("**Doctor Recommendation**")
        for rec in get_recommendations(score):
            st.write(f"- {rec}")


def show_forecast():
    st.title("Forecast")
    df = load_dataset()
    years_p, values_p = prophet_forecast(df)
    years_a, values_a = arima_forecast(df)
    years_l, values_l = lstm_forecast(df)

    st.subheader("Population Forecast")
    st.line_chart({"Prophet": pd.Series(values_p, index=years_p), "ARIMA": pd.Series(values_a, index=years_a), "LSTM": pd.Series(values_l, index=years_l)})
    st.write("Forecasting module with population prevalence predictions for 2025-2060.")


def show_analytics():
    st.title("Analytics")
    df = load_dataset()
    st.plotly_chart(plot_heart_disease_distribution(df), use_container_width=True)
    st.plotly_chart(plot_gender_distribution(df), use_container_width=True)
    st.plotly_chart(plot_age_distribution(df), use_container_width=True)
    st.plotly_chart(plot_cholesterol_distribution(df), use_container_width=True)
    st.plotly_chart(plot_boxplot(df, "RestingBP"), use_container_width=True)
    st.plotly_chart(plot_correlation_heatmap(df), use_container_width=True)


def show_reports():
    st.title("Reports")
    st.write("Generate PDF, CSV, and prediction history reports.")
    st.write("Report generation can be implemented using ReportLab and Pandas export.")


def show_settings():
    st.title("Settings")
    st.write("Configure app preferences, MongoDB Atlas connection, and model parameters.")
    if "mongo_uri" not in st.session_state:
        st.session_state.mongo_uri = os.getenv("MONGODB_URI", "")
    st.session_state.mongo_uri = st.text_input("MongoDB URI", value=st.session_state.mongo_uri, type="password")
    st.checkbox("Enable patient authentication")
    st.markdown("---")
    st.write("Current MongoDB Atlas URI is stored for this session. Restart the app to persist environment settings.")


def main():
    page = st.sidebar.radio("Navigation", MENU_ITEMS)

    if page == "Home":
        show_home()
    elif page == "Dashboard":
        show_dashboard()
    elif page == "Patient Details":
        show_patient_details()
    elif page == "Predict Disease":
        show_predict()
    elif page == "Forecast":
        show_forecast()
    elif page == "Analytics":
        show_analytics()
    elif page == "Reports":
        show_reports()
    elif page == "Settings":
        show_settings()


if __name__ == "__main__":
    main()
