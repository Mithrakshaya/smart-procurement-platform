import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import tensorflow as tf


# ==========================================================
# 1. Load dataset
# ==========================================================

DATA_FILE = "ai/data/grainflow_features.csv"

df = pd.read_csv(DATA_FILE)

print("Dataset shape:", df.shape)


# ==========================================================
# 2. Prepare features
# ==========================================================

targets = [
    "target_arrivals",
    "target_queue_length",
    "target_waiting_time"
]

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

X = X.select_dtypes(include=[np.number])


# ==========================================================
# 3. Time-based split
# ==========================================================

split_index = int(len(df) * 0.80)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]


# ==========================================================
# 4. Scale for Deep Learning
# ==========================================================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# ==========================================================
# 5. Model files
# ==========================================================

model_files = {
    "target_arrivals":
        "ai/models/saved_models/arrival_prediction_model.keras",

    "target_queue_length":
        "ai/models/saved_models/queue_prediction_model.keras",

    "target_waiting_time":
        "ai/models/saved_models/waiting_time_prediction_model.keras"
}


# ==========================================================
# 6. Compare models
# ==========================================================

results = []


for target in targets:

    print("\n======================================")
    print("Comparing:", target)
    print("======================================")

    y_train = df[target].iloc[:split_index]
    y_test = df[target].iloc[split_index:]


    # ------------------------------------------------------
    # Random Forest
    # ------------------------------------------------------

    rf_model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )

    rf_model.fit(
        X_train,
        y_train
    )

    rf_pred = rf_model.predict(X_test)

    rf_mae = mean_absolute_error(
        y_test,
        rf_pred
    )

    rf_rmse = np.sqrt(
        mean_squared_error(
            y_test,
            rf_pred
        )
    )

    rf_r2 = r2_score(
        y_test,
        rf_pred
    )


    # ------------------------------------------------------
    # Deep Learning
    # ------------------------------------------------------

    dl_model = tf.keras.models.load_model(
        model_files[target]
    )

    dl_pred = dl_model.predict(
        X_test_scaled,
        verbose=0
    ).flatten()

    dl_mae = mean_absolute_error(
        y_test,
        dl_pred
    )

    dl_rmse = np.sqrt(
        mean_squared_error(
            y_test,
            dl_pred
        )
    )

    dl_r2 = r2_score(
        y_test,
        dl_pred
    )


    # ------------------------------------------------------
    # Select best model
    # ------------------------------------------------------

    if rf_r2 >= dl_r2:
        selected = "Random Forest"
    else:
        selected = "Deep Learning"


    # ------------------------------------------------------
    # Print results
    # ------------------------------------------------------

    print("\nRandom Forest:")
    print(f"MAE  : {rf_mae:.4f}")
    print(f"RMSE : {rf_rmse:.4f}")
    print(f"R2   : {rf_r2:.4f}")

    print("\nDeep Learning:")
    print(f"MAE  : {dl_mae:.4f}")
    print(f"RMSE : {dl_rmse:.4f}")
    print(f"R2   : {dl_r2:.4f}")

    print("\nSelected model:", selected)


    results.append({
        "Prediction": target,
        "RF_MAE": round(rf_mae, 4),
        "RF_RMSE": round(rf_rmse, 4),
        "RF_R2": round(rf_r2, 4),
        "DL_MAE": round(dl_mae, 4),
        "DL_RMSE": round(dl_rmse, 4),
        "DL_R2": round(dl_r2, 4),
        "Selected_Model": selected
    })


# ==========================================================
# 7. Final comparison table
# ==========================================================

results_df = pd.DataFrame(results)


print("\n\n==============================================")
print("FINAL MODEL COMPARISON")
print("==============================================")

print(
    results_df.to_string(index=False)
)


# ==========================================================
# 8. Save results
# ==========================================================

OUTPUT_FILE = "ai/evaluation/model_comparison_results.csv"

results_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nComparison saved to:")
print(OUTPUT_FILE)