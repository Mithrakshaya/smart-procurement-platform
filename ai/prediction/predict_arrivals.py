import pandas as pd
import joblib
from pathlib import Path


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = BASE_DIR / "data" / "grainflow_features.csv"
MODEL_PATH = BASE_DIR / "models" / "saved_models" / "farmer_arrival_rf_model.joblib"
FEATURE_PATH = BASE_DIR / "models" / "saved_models" / "arrival_feature_names.joblib"


# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

def load_model():

    model = joblib.load(MODEL_PATH)
    feature_names = joblib.load(FEATURE_PATH)

    return model, feature_names


# --------------------------------------------------
# PREDICT FARMER ARRIVALS
# --------------------------------------------------

def predict_arrivals(input_data):

    model, feature_names = load_model()

    # Make sure input is a DataFrame
    if isinstance(input_data, dict):
        input_data = pd.DataFrame([input_data])

    # Check required features
    missing_features = [
        feature for feature in feature_names
        if feature not in input_data.columns
    ]

    if missing_features:
        raise ValueError(
            f"Missing required features: {missing_features}"
        )

    # Keep features in exactly the same order
    X = input_data[feature_names]

    # Prediction
    prediction = model.predict(X)

    return prediction


# --------------------------------------------------
# TEST THE FUNCTION
# --------------------------------------------------

if __name__ == "__main__":

    print("\n----------------------------------------")
    print("FARMER ARRIVAL PREDICTION TEST")
    print("----------------------------------------")

    # Load existing feature-engineered dataset
    df = pd.read_csv(DATA_PATH)

    print("Dataset loaded:", df.shape)

    # Take one sample row
    sample = df.iloc[[0]]

    # Actual value
    actual = sample["target_arrivals"].iloc[0]

    # Predict
    prediction = predict_arrivals(sample)

    predicted_value = prediction[0]

    print("\nActual farmer arrivals   :", round(actual, 2))
    print("Predicted farmer arrivals:", round(predicted_value, 2))

    print("\nPrediction function working successfully!")

    print("----------------------------------------")