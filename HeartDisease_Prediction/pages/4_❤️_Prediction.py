import streamlit as st

from utils.prediction import generate_prediction_report, predict_heart_disease, get_health_message

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
        "Sex": "F" if sex == "Female" else "M",
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
        }[rest_ecg],
        "MaxHR": int(max_hr),
        "ExerciseAngina": "Y" if exercise_angina == "Yes" else "N",
        "Oldpeak": float(oldpeak),
        "ST_Slope": {
            "Upsloping": "Up",
            "Flat": "Flat",
            "Downsloping": "Down",
        }[st_slope],
    }

    result = predict_heart_disease(input_values)
    health_message = get_health_message(result["probability"] / 100)

    st.divider()
    
    # Display Health Message Card
    st.markdown(
        f"""
        <div style="background-color: {health_message['bg_color']}; border-left: 5px solid {health_message['color']}; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h2 style="color: {health_message['color']}; margin-top: 0;">
                {health_message['title']}
            </h2>
            <p style="font-size: 16px; line-height: 1.6; color: #333; margin: 15px 0;">
                {health_message['message']}
            </p>
            <p style="font-style: italic; color: {health_message['color']}; font-weight: bold; margin: 15px 0;">
                💡 {health_message['motivational']}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Display Metrics
    st.divider()
    st.subheader("📊 Prediction Details")
    
    # Display Prediction Result
    if result["prediction"] == 1:
        st.error("❌ Heart Disease Detected")
    else:
        st.success("✅ No Heart Disease Detected")
    
    st.metric("Risk Level", health_message["risk_category"])
    
    # Display Probabilities
    st.subheader("📈 Confidence Scores")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Probability of Heart Disease", f"{result['probability']:.1f}%")
    with col2:
        st.metric("Probability of No Heart Disease", f"{100 - result['probability']:.1f}%")

    # Recommendations
    st.subheader("💪 Health Recommendations")
    for i, item in enumerate(result["recommendations"], 1):
        st.write(f"{i}. {item}")

    # Download Report
    st.divider()
    st.download_button(
        label="📄 Download Prediction Report",
        data=generate_prediction_report(input_values, result).getvalue(),
        file_name="prediction_report.pdf",
        mime="application/pdf",
    )
else:
    st.info("📋 Submit the form above to generate a personalized heart health prediction.")
