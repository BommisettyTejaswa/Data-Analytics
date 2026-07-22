import time

import streamlit as st

from utils.train_model import load_training_results, train_and_save_models

st.title("🤖 Model Training")

st.write("Train multiple classifiers and automatically save the best-performing model.")

if st.button("Train Model", type="primary"):
    progress = st.progress(0)
    status = st.empty()

    status.text("Loading Dataset...")
    progress.progress(20)
    time.sleep(0.5)

    status.text("Training Models...")
    progress.progress(60)
    result = train_and_save_models()

    status.text("Saving Best Model...")
    progress.progress(100)
    time.sleep(0.5)

    st.success("Training completed successfully!")
    st.metric("Best Model", result["best_model"])
    st.metric("Best Accuracy", f"{result['best_accuracy'] * 100:.2f}%")

    st.subheader("Training Results")
    st.dataframe(result["results"], use_container_width=True)
else:
    results = load_training_results()
    if results:
        st.success("A trained model is already available.")
        st.metric("Best Model", results["best_model"])
        st.metric("Best Accuracy", f"{results['best_accuracy'] * 100:.2f}%")
    else:
        st.info("No training results available yet. Click the button to train the model.")
