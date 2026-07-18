import os
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

TARGET_COLUMN = "HeartDisease"
DATASET_PATH = os.path.join("dataset", "heart.csv")


def load_dataset(path: str = DATASET_PATH) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Dataset not found at {path}")
    return pd.read_csv(path)


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned = cleaned.drop_duplicates().reset_index(drop=True)

    for column in cleaned.columns:
        if cleaned[column].dtype in ["float64", "int64", "float32", "int32"]:
            cleaned[column] = cleaned[column].fillna(cleaned[column].median())
        else:
            cleaned[column] = cleaned[column].fillna(cleaned[column].mode().iloc[0] if not cleaned[column].mode().empty else "Unknown")

    return cleaned


def get_feature_columns(df: pd.DataFrame) -> Tuple[List[str], List[str]]:
    feature_columns = [col for col in df.columns if col != TARGET_COLUMN]
    numeric_columns = df[feature_columns].select_dtypes(include=["number"]).columns.tolist()
    categorical_columns = [col for col in feature_columns if col not in numeric_columns]
    return numeric_columns, categorical_columns


def fit_preprocessors(X: pd.DataFrame) -> Dict[str, Any]:
    numeric_columns, categorical_columns = get_feature_columns(X)

    numeric_medians = {}
    categorical_fill_values = {}

    numeric_df = X[numeric_columns].copy()
    for column in numeric_columns:
        median_value = float(numeric_df[column].median())
        numeric_medians[column] = median_value
        numeric_df[column] = numeric_df[column].fillna(median_value)

    from sklearn.preprocessing import StandardScaler

    scaler = StandardScaler()
    scaler.fit(numeric_df)

    categorical_df = X[categorical_columns].copy()
    for column in categorical_columns:
        fill_value = str(categorical_df[column].mode().iloc[0]) if not categorical_df[column].mode().empty else "Unknown"
        categorical_fill_values[column] = fill_value
        categorical_df[column] = categorical_df[column].fillna(fill_value).astype(str)

    from sklearn.preprocessing import OneHotEncoder

    encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    encoder.fit(categorical_df)

    return {
        "scaler": scaler,
        "encoder": encoder,
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns,
        "numeric_medians": numeric_medians,
        "categorical_fill_values": categorical_fill_values,
    }


def transform_features(
    X: pd.DataFrame,
    scaler: Any,
    encoder: Any,
    numeric_columns: List[str],
    categorical_columns: List[str],
    numeric_medians: Dict[str, float],
    categorical_fill_values: Dict[str, str],
) -> np.ndarray:
    numeric_df = X[numeric_columns].copy()
    for column in numeric_columns:
        numeric_df[column] = numeric_df[column].fillna(numeric_medians.get(column, 0))

    categorical_df = X[categorical_columns].copy()
    for column in categorical_columns:
        categorical_df[column] = categorical_df[column].fillna(categorical_fill_values.get(column, "Unknown")).astype(str)

    numeric_array = scaler.transform(numeric_df)
    categorical_array = encoder.transform(categorical_df)
    return np.hstack([numeric_array, categorical_array])


def split_dataset(df: pd.DataFrame, test_size: float = 0.2) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    cleaned_df = clean_dataset(df)
    X = cleaned_df.drop(TARGET_COLUMN, axis=1)
    y = cleaned_df[TARGET_COLUMN]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42, stratify=y)
    return X_train, X_test, y_train, y_test
