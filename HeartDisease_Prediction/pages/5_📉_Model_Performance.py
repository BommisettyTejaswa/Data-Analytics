import streamlit as st

from utils.train_model import load_training_results

st.title("📉 Model Performance")

results = load_training_results()
if not results:
    st.info("Train the model first to view performance metrics.")
    st.stop()

metrics_df = st.session_state.get("metrics_df")
if metrics_df is None:
    metrics_df = results["results"]
    st.session_state["metrics_df"] = metrics_df

st.dataframe(metrics_df, use_container_width=True)

st.subheader("Best Model")
st.metric("Model", results["best_model"])
st.metric("Accuracy", f"{results['best_accuracy'] * 100:.2f}%")

if results.get("feature_importance"):
    st.subheader("Top Feature Importance")
    st.dataframe(results["feature_importance"], use_container_width=True)
