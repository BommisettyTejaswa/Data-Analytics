import streamlit as st

from utils.prediction import generate_prediction_report, predict_heart_disease

st.title("❤️ Heart Disease Prediction")

st.write("Enter patient details to estimate the likelihood of heart disease.")

with st.form("prediction_form"):
    age = st.number_input("Age", min_value=18, max_value=100, value=50)
    sex = st.selectbox("Gender", ["Female", "Male"])
    chest_pain = st.selectbox("Chest Pain", ["Typical Angina", "Atypical Angina", "Non-Anginal Pain", "Asymptomatic"])
    resting_bp = st.number_input("Resting BP", min_value=80, max_value=220, value=120)
    cholesterol = st.number_input("Cholesterol", min_value=100, max_value=600, value=200)
    fasting_bs = st.selectbox("Fasting Blood Sugar", ["No", "Yes"])
    rest_ecg = st.selectbox("Rest ECG", ["Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"])
    max_hr = st.number_input("Maximum Heart Rate", min_value=60, max_value=220, value=150)
    exercise_angina = st.selectbox("Exercise Angina", ["No", "Yes"])
    oldpeak = st.number_input("Old Peak", min_value=0.0, max_value=8.0, value=1.0, step=0.1)
    st_slope = st.selectbox("ST Slope", ["Upsloping", "Flat", "Downsloping"])

    submitted = st.form_submit_button("Predict", type="primary")

if submitted:
    input_values = {
        "Age": int(age),
        "Sex": 0 if sex == "Female" else 1,
        "ChestPainType": ["TA", "ATA", "NAP", "ASYM"].index({"Typical Angina": "TA", "Atypical Angina": "ATA", "Non-Anginal Pain": "NAP", "Asymptomatic": "ASYM"}[chest_pain]),
        "RestingBP": int(resting_bp),
        "Cholesterol": int(cholesterol),
        "FastingBS": 1 if fasting_bs == "Yes" else 0,
        "RestingECG": ["Normal", "ST", "LVH"].index({"Normal": "Normal", "ST-T Wave Abnormality": "ST", "Left Ventricular Hypertrophy": "LVH"}[rest_ecg]),
        "MaxHR": int(max_hr),
        "ExerciseAngina": 1 if exercise_angina == "Yes" else 0,
        "Oldpeak": float(oldpeak),
        "ST_Slope": ["Up", "Flat", "Down"].index({"Upsloping": "Up", "Flat": "Flat", "Downsloping": "Down"}[st_slope]),
    }

    result = predict_heart_disease(input_values)

    st.subheader("Prediction")
    st.metric("Probability", f"{result['probability']}%")
    st.metric("Risk Level", result["risk_level"])

    if result["prediction"] == 1:
        st.error("Heart Disease Likely")
    else:
        st.success("No Heart Disease Detected")

    st.subheader("Recommendations")
    for item in result["recommendations"]:
        st.write(f"• {item}")

    st.download_button(
        label="Download Prediction Report",
        data=generate_prediction_report(input_values, result).getvalue(),
        file_name="prediction_report.pdf",
        mime="application/pdf",
    )
else:
    st.info("Submit the form to generate a prediction.")
