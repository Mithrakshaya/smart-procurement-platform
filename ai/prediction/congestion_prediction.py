import pandas as pd
import joblib
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = BASE_DIR / "data" / "grainflow_features.csv"

MODEL_DIR = BASE_DIR / "models" / "saved_models"

MODEL_PATH = MODEL_DIR / "congestion_rf_model.joblib"
FEATURE_PATH = MODEL_DIR / "congestion_feature_names.joblib"


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = pd.read_csv(DATA_PATH)

print("Dataset loaded:", df.shape)


# --------------------------------------------------
# TARGET
# --------------------------------------------------

TARGET = "target_congestion_score"


# --------------------------------------------------
# EXCLUDE TARGET / LEAKAGE COLUMNS
# --------------------------------------------------

target_columns = [
    "target_arrivals",
    "target_queue_length",
    "target_waiting_time",
    "target_congestion_score",
    "target_congestion_level"
]

leakage_columns = [
    "queue_length",
    "average_waiting_time"
]

excluded_columns = target_columns + leakage_columns


# --------------------------------------------------
# FEATURES
# --------------------------------------------------

X = df.drop(
    columns=excluded_columns,
    errors="ignore"
)

y = df[TARGET]

# Keep numerical features only
X = X.select_dtypes(
    include=["number"]
)


print("\nFeatures used:")
print(list(X.columns))

print("\nNumber of features:", X.shape[1])


# --------------------------------------------------
# TIME-BASED TRAIN/TEST SPLIT
# --------------------------------------------------

split_index = int(len(df) * 0.80)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]


print("\nTraining rows:", len(X_train))
print("Testing rows :", len(X_test))


# --------------------------------------------------
# TRAIN RANDOM FOREST
# --------------------------------------------------

print("\nTraining Congestion Prediction model...")

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

model.fit(
    X_train,
    y_train
)


# --------------------------------------------------
# PREDICTION
# --------------------------------------------------

predictions = model.predict(X_test)


# --------------------------------------------------
# EVALUATION
# --------------------------------------------------

mae = mean_absolute_error(
    y_test,
    predictions
)

rmse = np.sqrt(
    mean_squared_error(
        y_test,
        predictions
    )
)

r2 = r2_score(
    y_test,
    predictions
)


print("\n======================================")
print("CONGESTION MODEL RESULTS")
print("======================================")

print(f"MAE  : {mae:.4f}")
print(f"RMSE : {rmse:.4f}")
print(f"R2   : {r2:.4f}")


# --------------------------------------------------
# SAMPLE PREDICTIONS
# --------------------------------------------------

print("\nTest prediction sample:")

for actual, predicted in zip(
    y_test.iloc[:10],
    predictions[:10]
):

    print(
        f"Actual: {actual:.2f} | "
        f"Predicted: {predicted:.2f}"
    )


# --------------------------------------------------
# SAVE MODEL
# --------------------------------------------------

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

joblib.dump(
    model,
    MODEL_PATH
)

joblib.dump(
    list(X.columns),
    FEATURE_PATH
)


# --------------------------------------------------
# FINAL
# --------------------------------------------------

print("\n======================================")
print("CONGESTION MODEL READY")
print("======================================")

print("Model saved to:")
print(MODEL_PATH)

print("\nFeature names saved to:")
print(FEATURE_PATH)