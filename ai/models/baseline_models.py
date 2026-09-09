# ============================================================
# GRAINFLOW BASELINE ML MODELS
# Member 3 - AI Prediction & Queue Management
# ============================================================

import os
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ============================================================
# 1. LOAD DATASET
# ============================================================

DATA_PATH = os.path.join(
    "ai",
    "data",
    "grainflow_features.csv"
)

print("=" * 60)
print("GRAINFLOW BASELINE ML MODELS")
print("=" * 60)

print("\nLoading dataset...")
print("Path:", DATA_PATH)

df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)


# ============================================================
# 2. DEFINE TARGETS
# ============================================================

target_columns = [
    "target_arrivals",
    "target_queue_length",
    "target_waiting_time",
    "target_congestion_score",
    "target_congestion_level"
]


# ============================================================
# 3. REMOVE TARGET / LEAKAGE COLUMNS
# ============================================================

excluded_columns = [
    # Future target values
    "target_arrivals",
    "target_queue_length",
    "target_waiting_time",
    "target_congestion_score",
    "target_congestion_level",

    # Operational values too closely tied to future queue/waiting targets
    "queue_length",
    "average_waiting_time"
]

X = df.drop(columns=excluded_columns)

print("\nFeatures used for prediction:")
print(list(X.columns))

print("\nNumber of features:", X.shape[1])


# ============================================================
# 4. SELECT REGRESSION TARGETS
# ============================================================

targets = [
    "target_arrivals",
    "target_queue_length",
    "target_waiting_time"
]


# ============================================================
# 5. REMOVE NON-NUMERIC COLUMNS
# ============================================================

# The preprocessing stage should already encode categorical
# columns, but this check prevents unexpected object columns
# from breaking Random Forest.

non_numeric_columns = X.select_dtypes(
    include=["object"]
).columns.tolist()

if len(non_numeric_columns) > 0:

    print("\nRemoving non-numeric columns:")
    print(non_numeric_columns)

    X = X.drop(columns=non_numeric_columns)

else:

    print("\nAll model features are numeric.")


# ============================================================
# 6. TIME-BASED TRAIN / TEST SPLIT
# ============================================================

# This is a forecasting project.
# Therefore, we should train on earlier records and test
# on later records instead of randomly mixing past and future.

split_index = int(len(df) * 0.80)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]


print("\nTime-based split:")
print("Training rows:", len(X_train))
print("Testing rows :", len(X_test))


# ============================================================
# 7. TRAIN MODELS
# ============================================================

for target in targets:

    print("\n" + "-" * 60)
    print("Training model for:", target)
    print("-" * 60)

    y = df[target]

    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    # Predictions
    predictions = model.predict(X_test)

    # Evaluation
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

    print("MAE  :", round(mae, 4))
    print("RMSE :", round(rmse, 4))
    print("R2   :", round(r2, 4))


# ============================================================
# 8. COMPLETE
# ============================================================

print("\n" + "=" * 60)
print("BASELINE MODEL TRAINING COMPLETE")
print("=" * 60)