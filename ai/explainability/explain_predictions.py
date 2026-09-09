import joblib
import pandas as pd
from pathlib import Path


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_DIR = (
    BASE_DIR
    / "models"
    / "saved_models"
)

DATA_PATH = (
    BASE_DIR
    / "data"
    / "grainflow_features.csv"
)


# --------------------------------------------------
# MODEL FILES
# --------------------------------------------------

MODELS = {
    "Farmer Arrival": (
        MODEL_DIR / "farmer_arrival_rf_model.joblib",
        MODEL_DIR / "arrival_feature_names.joblib"
    ),

    "Queue Length": (
        MODEL_DIR / "queue_length_rf_model.joblib",
        MODEL_DIR / "queue_feature_names.joblib"
    ),

    "Waiting Time": (
        MODEL_DIR / "waiting_time_rf_model.joblib",
        MODEL_DIR / "waiting_time_feature_names.joblib"
    ),

    "Congestion": (
        MODEL_DIR / "congestion_rf_model.joblib",
        MODEL_DIR / "congestion_feature_names.joblib"
    )
}


# --------------------------------------------------
# EXPLAIN MODEL
# --------------------------------------------------

def explain_model(model_name, top_n=10):

    model_path, feature_path = MODELS[model_name]

    # Load model
    model = joblib.load(model_path)

    # Load feature names
    feature_names = joblib.load(feature_path)

    # Get feature importance
    importance = model.feature_importances_

    # Create DataFrame
    importance_df = pd.DataFrame({
        "feature": feature_names,
        "importance": importance
    })

    # Sort from highest to lowest
    importance_df = importance_df.sort_values(
        by="importance",
        ascending=False
    )

    return importance_df.head(top_n)


# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":

    print("\n======================================")
    print("EXPLAINABLE AI - FEATURE IMPORTANCE")
    print("======================================")

    # Check dataset
    df = pd.read_csv(DATA_PATH)

    print(
        "Dataset loaded:",
        df.shape
    )

    # Explain each model
    for model_name in MODELS:

        print("\n--------------------------------------")
        print(model_name)
        print("--------------------------------------")

        importance_df = explain_model(
            model_name,
            top_n=10
        )

        print(
            importance_df.to_string(
                index=False
            )
        )

    print("\n======================================")
    print("EXPLAINABLE AI COMPLETED")
    print("======================================")