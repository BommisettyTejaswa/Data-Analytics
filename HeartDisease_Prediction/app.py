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


def get_prediction_suggestions(probability: float, prediction: int):
    if prediction == 1:
        if probability >= 0.8:
            return [
                "Seek urgent cardiology evaluation.",
                "Schedule a full diagnostic workup, including ECG and stress testing.",
                "Review medications and lifestyle with your doctor.",
            ]
        if probability >= 0.6:
            return [
                "Schedule a medical consultation soon.",
                "Increase physical activity and reduce sodium intake.",
                "Monitor blood pressure and cholesterol regularly.",
            ]
        return [
            "Discuss your risk with a physician.",
            "Maintain a healthy diet and monitor symptoms.",
            "Stay consistent with follow-up appointments.",
        ]

    if probability >= 0.6:
        return [
            "Continue monitoring your cardiovascular health closely.",
            "Adopt a balanced diet and regular exercise routine.",
            "Talk to a healthcare provider about preventive lifestyle changes.",
        ]

    return [
        "Keep up your healthy habits.",
        "Maintain a balanced diet and regular physical activity.",
        "Schedule routine health checkups as recommended.",
    ]


def get_doctor_advice(probability: float, prediction: int):
    """Return doctor-style lifestyle advice (diet, exercise, yoga) based on
    predicted probability and binary prediction.
    probability: float between 0 and 1
    prediction: 0 or 1
    """
    if prediction == 1:
        if probability >= 0.8:
            return {
                "diet": [
                    "Avoid processed and fried foods; prefer steamed/grilled options.",
                    "Increase intake of fruits, vegetables, whole grains, and legumes.",
                    "Limit saturated fats and replace with healthy fats (olive oil, nuts).",
                    "Reduce sodium intake; avoid packaged high-salt snacks.",
                ],
                "exercise": [
                    "Consult a physician before starting intense exercise.",
                    "Begin gentle cardiovascular activities (walking, stationary bike) 10-20 min daily.",
                    "Gradually increase to 30 minutes of moderate activity most days as tolerated.",
                ],
                "yoga": [
                    "Practice gentle yoga (Hatha, Yin) focusing on breath and relaxation.",
                    "Incorporate restorative poses and avoid extreme inversions or breath-holding.",
                    "Try guided pranayama (deep diaphragmatic breathing) for stress reduction.",
                ],
            }
        if probability >= 0.6:
            return {
                "diet": [
                    "Adopt a Mediterranean-style diet: fish, olive oil, vegetables, and whole grains.",
                    "Reduce red meat and sugary beverages.",
                    "Choose low-fat dairy and increase fiber-rich foods.",
                ],
                "exercise": [
                    "Aim for 20-30 minutes of brisk walking most days.",
                    "Include light resistance training (bodyweight or bands) twice weekly.",
                    "Avoid sudden intense exertion until medically cleared.",
                ],
                "yoga": [
                    "Start a gentle flow (Vinyasa/Hatha) 2–3 times/week to improve mobility.",
                    "Practice calming breathing techniques after sessions.",
                ],
            }
        return {
            "diet": [
                "Follow balanced meals with lean protein and vegetables.",
                "Limit processed snacks and added sugars.",
            ],
            "exercise": [
                "Maintain regular moderate activity: 30 minutes of walking most days.",
                "Include flexibility and balance exercises.",
            ],
            "yoga": [
                "Try basic Hatha sequences focusing on flexibility and relaxation.",
            ],
        }

    # prediction == 0 (no disease predicted)
    if probability >= 0.6:
        return {
            "diet": [
                "Maintain a heart-healthy diet (fruits, vegetables, whole grains).",
                "Keep saturated fats and added sugars low.",
            ],
            "exercise": [
                "Continue regular aerobic exercise (walking, cycling) 150 minutes/week.",
                "Add strength training 2x/week.",
            ],
            "yoga": [
                "Use yoga to support flexibility and stress management (20-30 min sessions).",
            ],
        }

    return {
        "diet": [
            "Keep up a balanced diet rich in plants and lean proteins.",
            "Limit processed foods and maintain portion control.",
        ],
        "exercise": [
            "Aim for at least 150 minutes of moderate aerobic activity weekly.",
            "Include mobility and light strength work to stay active.",
        ],
        "yoga": [
            "Incorporate short daily stretches or a 15–20 minute gentle yoga routine for wellbeing.",
        ],
    }


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
        chest_pain = st.selectbox(
            "Chest Pain Type",
            ["Typical Angina", "Atypical Angina", "Non-Anginal Pain", "Asymptomatic"],
        )
        resting_bp = st.number_input("Resting Blood Pressure", min_value=80, max_value=220, value=120)
        cholesterol = st.number_input("Cholesterol", min_value=100, max_value=600, value=200)
        fasting_bs = st.selectbox("Fasting Blood Sugar", ["No", "Yes"])
        resting_ecg = st.selectbox("Resting ECG", ["Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"])
        max_hr = st.number_input("Max Heart Rate", min_value=60, max_value=220, value=150)
        exercise_angina = st.selectbox("Exercise Angina", ["No", "Yes"])
        oldpeak = st.number_input("Old Peak", min_value=0.0, max_value=8.0, value=1.0, step=0.1)
        st_slope = st.selectbox("ST Slope", ["Upsloping", "Flat", "Downsloping"])
        submitted = st.form_submit_button("Predict")

    if submitted:
        input_values = {
            "Age": int(age),
            "Sex": "F" if gender == "Female" else "M",
            "ChestPainType": {
                "Typical Angina": "TA",
                "Atypical Angina": "ATA",
                "Non-Anginal Pain": "NAP",
                "Asymptomatic": "ASY",
            }[chest_pain],
            "RestingBP": int(resting_bp),
            "Cholesterol": int(cholesterol),
            "FastingBS": 1 if fasting_bs == "Yes" else 0,
            "RestingECG": {
                "Normal": "Normal",
                "ST-T Wave Abnormality": "ST",
                "Left Ventricular Hypertrophy": "LVH",
            }[resting_ecg],
            "MaxHR": int(max_hr),
            "ExerciseAngina": "Y" if exercise_angina == "Yes" else "N",
            "Oldpeak": float(oldpeak),
            "ST_Slope": {
                "Upsloping": "Up",
                "Flat": "Flat",
                "Downsloping": "Down",
            }[st_slope],
        }

        try:
            result = predict_heart_disease(input_values)
            st.success("Prediction completed.")
            # Probability intentionally hidden on UI; show risk level only
            st.metric("Risk Level", result["risk_level"])

            if result["prediction"] == 1:
                st.error("Heart Disease Likely")
            else:
                st.success("No Heart Disease Detected")

            st.subheader("Recommendations")
            for rec in result["recommendations"]:
                st.write(f"- {rec}")

            st.subheader("Suggested Next Steps")
            suggestions = get_prediction_suggestions(result["probability"] / 100, result["prediction"])
            for suggestion in suggestions:
                st.write(f"- {suggestion}")
        except Exception as exc:
            st.error(f"Prediction failed: {exc}")


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
