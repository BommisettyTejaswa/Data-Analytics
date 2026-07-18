import json
import os
from typing import Any, Dict, List, Tuple

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC

from utils.preprocessing import TARGET_COLUMN, clean_dataset, fit_preprocessors, load_dataset, split_dataset, transform_features

MODELS_DIR = "models"
RESULTS_PATH = os.path.join(MODELS_DIR, "training_results.json")


def _build_model_configs() -> List[Tuple[str, Any]]:
    models: List[Tuple[str, Any]] = [
        ("Logistic Regression", LogisticRegression(max_iter=2000, random_state=42)),
        ("Decision Tree", DecisionTreeClassifier(random_state=42)),
        ("Random Forest", RandomForestClassifier(n_estimators=150, random_state=42)),
        ("SVM", SVC(probability=True, random_state=42)),
    ]

    try:
        from xgboost import XGBClassifier

        models.append(("XGBoost", XGBClassifier(n_estimators=120, learning_rate=0.1, max_depth=3, random_state=42)))
    except Exception:
        pass

    return models


def train_and_save_models(dataset_path: str = "dataset/heart.csv") -> Dict[str, Any]:
    os.makedirs(MODELS_DIR, exist_ok=True)
    df = clean_dataset(load_dataset(dataset_path))
    X_train, X_test, y_train, y_test = split_dataset(df, test_size=0.2)

    preprocessor = fit_preprocessors(X_train)
    X_train_processed = transform_features(
        X_train,
        preprocessor["scaler"],
        preprocessor["encoder"],
        preprocessor["numeric_columns"],
        preprocessor["categorical_columns"],
        preprocessor["numeric_medians"],
        preprocessor["categorical_fill_values"],
    )
    X_test_processed = transform_features(
        X_test,
        preprocessor["scaler"],
        preprocessor["encoder"],
        preprocessor["numeric_columns"],
        preprocessor["categorical_columns"],
        preprocessor["numeric_medians"],
        preprocessor["categorical_fill_values"],
    )

    results = []
    best_model_payload: Dict[str, Any] | None = None
    best_metrics: Dict[str, Any] | None = None

    for name, model in _build_model_configs():
        model.fit(X_train_processed, y_train)
        predictions = model.predict(X_test_processed)

        metrics = {
            "model": name,
            "accuracy": round(float(accuracy_score(y_test, predictions)), 4),
            "precision": round(float(precision_score(y_test, predictions, zero_division=0)), 4),
            "recall": round(float(recall_score(y_test, predictions, zero_division=0)), 4),
            "f1_score": round(float(f1_score(y_test, predictions, zero_division=0)), 4),
            "roc_auc": round(float(roc_auc_score(y_test, model.predict_proba(X_test_processed)[:, 1])), 4),
        }
        results.append(metrics)

        if best_metrics is None or metrics["accuracy"] > best_metrics["accuracy"]:
            best_metrics = metrics
            best_model_payload = {
                "model": model,
                "model_name": name,
                "preprocessor": preprocessor,
                "feature_names": list(preprocessor["numeric_columns"]) + list(preprocessor["encoder"].get_feature_names_out(preprocessor["categorical_columns"])),
            }

    if best_model_payload is None or best_metrics is None:
        raise RuntimeError("Training failed to produce a model")

    joblib.dump({"scaler": preprocessor["scaler"], "numeric_columns": preprocessor["numeric_columns"], "numeric_medians": preprocessor["numeric_medians"]}, os.path.join(MODELS_DIR, "scaler.pkl"))
    joblib.dump({"encoder": preprocessor["encoder"], "categorical_columns": preprocessor["categorical_columns"], "categorical_fill_values": preprocessor["categorical_fill_values"]}, os.path.join(MODELS_DIR, "encoder.pkl"))
    joblib.dump({"model": best_model_payload["model"], "model_name": best_model_payload["model_name"], "feature_names": best_model_payload["feature_names"]}, os.path.join(MODELS_DIR, "heart_model.pkl"))

    feature_importance = []
    if hasattr(best_model_payload["model"], "feature_importances_"):
        feature_importance = [
            {"feature": feature, "importance": round(float(importance), 4)}
            for feature, importance in zip(best_model_payload["feature_names"], best_model_payload["model"].feature_importances_)
        ]
        feature_importance = sorted(feature_importance, key=lambda item: item["importance"], reverse=True)[:10]

    payload = {
        "dataset_shape": list(df.shape),
        "best_model": best_metrics["model"],
        "best_accuracy": best_metrics["accuracy"],
        "results": results,
        "feature_importance": feature_importance,
    }

    with open(RESULTS_PATH, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)

    return payload


def load_training_results() -> Dict[str, Any]:
    if not os.path.exists(RESULTS_PATH):
        return {}
    with open(RESULTS_PATH, "r", encoding="utf-8") as handle:
        return json.load(handle)
