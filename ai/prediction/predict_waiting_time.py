import pandas as pd
import joblib
from pathlib import Path


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = (
    BASE_DIR
    / "data"
    / "grainflow_features.csv"
)

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "saved_models"
    / "waiting_time_rf_model.joblib"
)

FEATURE_PATH = (
    BASE_DIR
    / "models"
    / "saved_models"
    / "waiting_time_feature_names.joblib"
)


# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

def load_model():

    model = joblib.load(MODEL_PATH)

    feature_names = joblib.load(FEATURE_PATH)

    return model, feature_names


# --------------------------------------------------
# PREDICT WAITING TIME
# --------------------------------------------------

def predict_waiting_time(input_data):

    model, feature_names = load_model()

    # Convert dictionary to DataFrame
    if isinstance(input_data, dict):
        input_data = pd.DataFrame([input_data])

    # Check required features
    missing_features = [
        feature
        for feature in feature_names
        if feature not in input_data.columns
    ]

    if missing_features:

        raise ValueError(
            f"Missing required features: {missing_features}"
        )

    # Keep the exact feature order
    X = input_data[feature_names]

    # Prediction
    prediction = model.predict(X)

    return prediction


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    print("\n----------------------------------------")
    print("WAITING-TIME PREDICTION TEST")
    print("----------------------------------------")

    # Load feature-engineered dataset
    df = pd.read_csv(DATA_PATH)

    print("Dataset loaded:", df.shape)

    # Select one sample
    sample = df.iloc[[0]]

    # Actual waiting time
    actual = sample[
        "target_waiting_time"
    ].iloc[0]

    # Predict
    prediction = predict_waiting_time(sample)

    predicted_value = prediction[0]

    print(
        "\nActual waiting time   :",
        round(actual, 2)
    )

    print(
        "Predicted waiting time:",
        round(predicted_value, 2)
    )

    print(
        "\nWaiting-time prediction "
        "function working successfully!"
    )

    print("----------------------------------------")