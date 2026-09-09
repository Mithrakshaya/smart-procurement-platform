import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
import joblib
import os


# ==========================================================
# 1. Load dataset
# ==========================================================

DATA_FILE = "ai/data/grainflow_features.csv"

df = pd.read_csv(DATA_FILE)

print("Dataset loaded:", df.shape)


# ==========================================================
# 2. Define target
# ==========================================================

TARGET = "target_arrivals"


# ==========================================================
# 3. Remove target/leakage columns
# ==========================================================

excluded_columns = [
    "target_arrivals",
    "target_queue_length",
    "target_waiting_time",
    "target_congestion_score",
    "target_congestion_level",

    "queue_length",
    "average_waiting_time"
]


X = df.drop(
    columns=excluded_columns,
    errors="ignore"
)

y = df[TARGET]


# Keep numerical features
X = X.select_dtypes(include=[np.number])


print("\nFeatures used:")
print(list(X.columns))

print("\nNumber of features:", X.shape[1])


# ==========================================================
# 4. Time-based training data
# ==========================================================

split_index = int(len(df) * 0.80)

X_train = X.iloc[:split_index]
y_train = y.iloc[:split_index]

X_test = X.iloc[split_index:]
y_test = y.iloc[split_index:]


print("\nTraining rows:", len(X_train))
print("Testing rows :", len(X_test))


# ==========================================================
# 5. Train Random Forest
# ==========================================================

print("\nTraining Farmer Arrival Prediction model...")

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

model.fit(
    X_train,
    y_train
)


# ==========================================================
# 6. Test prediction
# ==========================================================

test_predictions = model.predict(X_test)


print("\nTest prediction sample:")

for actual, predicted in zip(
    y_test.head(10),
    test_predictions[:10]
):
    print(
        f"Actual: {actual:.2f} | "
        f"Predicted: {predicted:.2f}"
    )


# ==========================================================
# 7. Save model
# ==========================================================

MODEL_DIR = "ai/models/saved_models"

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)

MODEL_FILE = os.path.join(
    MODEL_DIR,
    "farmer_arrival_rf_model.joblib"
)

joblib.dump(
    model,
    MODEL_FILE
)


# ==========================================================
# 8. Save feature names
# ==========================================================

FEATURE_FILE = os.path.join(
    MODEL_DIR,
    "arrival_feature_names.joblib"
)

joblib.dump(
    list(X.columns),
    FEATURE_FILE
)


print("\n======================================")
print("FARMER ARRIVAL MODEL READY")
print("======================================")

print("Model saved to:")
print(MODEL_FILE)

print("\nFeature names saved to:")
print(FEATURE_FILE)