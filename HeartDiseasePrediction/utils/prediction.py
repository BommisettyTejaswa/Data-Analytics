import os
from io import BytesIO
from typing import Any, Dict, List

import joblib
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from utils.preprocessing import TARGET_COLUMN, transform_features

MODELS_DIR = "models"


def load_model_artifacts() -> Dict[str, Any]:
    scaler = joblib.load(os.path.join(MODELS_DIR, "scaler.pkl"))
    encoder = joblib.load(os.path.join(MODELS_DIR, "encoder.pkl"))
    model = joblib.load(os.path.join(MODELS_DIR, "heart_model.pkl"))
    return {"scaler": scaler, "encoder": encoder, "model": model}


def predict_heart_disease(input_values: Dict[str, Any]) -> Dict[str, Any]:
    artifacts = load_model_artifacts()
    input_df = pd.DataFrame([input_values])
    transformed = transform_features(
        input_df,
        artifacts["scaler"]["scaler"],
        artifacts["encoder"]["encoder"],
        artifacts["scaler"]["numeric_columns"],
        artifacts["encoder"]["categorical_columns"],
        artifacts["scaler"]["numeric_medians"],
        artifacts["encoder"]["categorical_fill_values"],
    )
    probability = float(artifacts["model"]["model"].predict_proba(transformed)[0, 1])
    prediction = int(probability >= 0.5)

    return {
        "prediction": prediction,
        "probability": round(probability * 100, 2),
        "risk_level": risk_level(probability),
        "recommendations": get_recommendations(probability),
    }


def risk_level(probability: float) -> str:
    if probability >= 0.8:
        return "VERY HIGH"
    if probability >= 0.6:
        return "HIGH"
    if probability >= 0.4:
        return "MODERATE"
    return "LOW"


def get_recommendations(probability: float) -> List[str]:
    if probability >= 0.8:
        return [
            "Seek urgent cardiology evaluation.",
            "Monitor blood pressure and cholesterol regularly.",
            "Avoid smoking and reduce saturated fats.",
        ]
    if probability >= 0.6:
        return [
            "Schedule a medical consultation soon.",
            "Increase daily physical activity.",
            "Reduce salt intake and maintain a healthy diet.",
        ]
    if probability >= 0.4:
        return [
            "Maintain regular exercise and a balanced diet.",
            "Monitor your blood pressure and resting heart rate.",
            "Visit a clinician for routine screening.",
        ]
    return [
        "Stay active and keep heart health habits consistent.",
        "Continue annual health checkups.",
        "Track your cardiovascular risk factors.",
    ]


def generate_prediction_report(input_values: Dict[str, Any], prediction_result: Dict[str, Any]) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("Title", parent=styles["Heading1"], textColor="#D90429", spaceAfter=12)
    body_style = styles["BodyText"]

    story = [
        Paragraph("Heart Disease Prediction Report", title_style),
        Paragraph("Generated from the Streamlit application", body_style),
        Spacer(1, 12),
        Paragraph(f"Prediction: {'Positive' if prediction_result['prediction'] == 1 else 'Negative'}", body_style),
        Paragraph(f"Probability: {prediction_result['probability']}%", body_style),
        Paragraph(f"Risk Level: {prediction_result['risk_level']}", body_style),
        Spacer(1, 12),
        Paragraph("Patient Inputs", styles["Heading2"]),
    ]

    data = [["Field", "Value"]]
    for key, value in input_values.items():
        data.append([key, str(value)])

    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), "#D90429"),
        ("TEXTCOLOR", (0, 0), (-1, 0), "white"),
        ("GRID", (0, 0), (-1, -1), 0.5, "#cccccc"),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(table)
    story.append(Spacer(1, 12))
    story.append(Paragraph("Recommendations", styles["Heading2"]))
    for item in prediction_result["recommendations"]:
        story.append(Paragraph(f"• {item}", body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer
