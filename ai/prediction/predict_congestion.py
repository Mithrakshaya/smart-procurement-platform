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
    / "congestion_rf_model.joblib"
)

FEATURE_PATH = (
    BASE_DIR
    / "models"
    / "saved_models"
    / "congestion_feature_names.joblib"
)


# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

def load_model():

    model = joblib.load(MODEL_PATH)

    feature_names = joblib.load(FEATURE_PATH)

    return model, feature_names


# --------------------------------------------------
# PREDICT CONGESTION SCORE
# --------------------------------------------------

def predict_congestion(input_data):

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

    # Keep exact feature order
    X = input_data[feature_names]

    # Prediction
    prediction = model.predict(X)

    # Keep score within 0-100
    prediction = prediction.clip(0, 100)

    return prediction


# --------------------------------------------------
# CONGESTION LEVEL
# --------------------------------------------------

def get_congestion_level(score):

    if score < 35:
        return "LOW"

    elif score < 65:
        return "MEDIUM"

    else:
        return "HIGH"


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    print("\n----------------------------------------")
    print("CONGESTION PREDICTION TEST")
    print("----------------------------------------")

    # Load feature-engineered dataset
    df = pd.read_csv(DATA_PATH)

    print("Dataset loaded:", df.shape)

    # Select one sample
    sample = df.iloc[[0]]

    # Actual score
    actual = sample[
        "target_congestion_score"
    ].iloc[0]

    # Predict
    prediction = predict_congestion(sample)

    predicted_score = prediction[0]

    # Convert score to level
    congestion_level = get_congestion_level(
        predicted_score
    )

    print(
        "\nActual congestion score   :",
        round(actual, 2)
    )

    print(
        "Predicted congestion score:",
        round(predicted_score, 2)
    )

    print(
        "Predicted congestion level:",
        congestion_level
    )

    print(
        "\nCongestion prediction "
        "function working successfully!"
    )

    print("----------------------------------------")