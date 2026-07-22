import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def plot_heart_disease_distribution(df: pd.DataFrame):
    counts = df["HeartDisease"].value_counts().reset_index()
    counts.columns = ["HeartDisease", "Count"]
    counts["HeartDisease"] = counts["HeartDisease"].map({1: "Disease", 0: "No Disease"})
    return px.bar(counts, x="HeartDisease", y="Count", color="HeartDisease", title="Heart Disease Distribution")


def plot_gender_distribution(df: pd.DataFrame):
    gender_series = df["Sex"].astype(str).str.strip().str.upper()
    gender_labels = gender_series.map({
        "M": "Male",
        "MALE": "Male",
        "1": "Male",
        "F": "Female",
        "FEMALE": "Female",
        "0": "Female",
    }).fillna("Unknown")

    counts = pd.DataFrame({
        "Gender": gender_labels.value_counts().index.tolist(),
        "Count": gender_labels.value_counts().values.tolist(),
    })

    if counts.empty:
        counts = pd.DataFrame({"Gender": ["Unknown"], "Count": [0]})

    return px.pie(counts, values="Count", names="Gender", title="Gender Distribution")


def plot_age_distribution(df: pd.DataFrame):
    return px.histogram(df, x="Age", nbins=20, title="Age Distribution")


def plot_chest_pain_analysis(df: pd.DataFrame):
    counts = df["ChestPainType"].value_counts().reset_index()
    counts.columns = ["ChestPainType", "Count"]
    return px.bar(counts, x="ChestPainType", y="Count", color="ChestPainType", title="Chest Pain Type Analysis")


def plot_cholesterol_distribution(df: pd.DataFrame):
    return px.histogram(df, x="Cholesterol", nbins=20, title="Cholesterol Distribution")


def plot_max_hr_distribution(df: pd.DataFrame):
    return px.histogram(df, x="MaxHR", nbins=20, title="Maximum Heart Rate Distribution")


def plot_correlation_heatmap(df: pd.DataFrame):
    numeric_df = df.select_dtypes(include=["number"])
    corr = numeric_df.corr()
    return px.imshow(corr, title="Correlation Heatmap")


def plot_boxplot(df: pd.DataFrame, column: str):
    return px.box(df, x="HeartDisease", y=column, color="HeartDisease", title=f"{column} by Heart Disease")


def plot_histogram(df: pd.DataFrame, column: str):
    return px.histogram(df, x=column, color="HeartDisease", barmode="overlay", title=f"{column} Distribution")
