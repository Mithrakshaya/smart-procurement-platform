import pandas as pd
import numpy as np
import tensorflow as tf

from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ==========================================================
# 1. Load dataset
# ==========================================================

DATA_FILE = "ai/data/grainflow_features.csv"
MODEL_FILE = "ai/models/saved_models/arrival_prediction_model.keras"

df = pd.read_csv(DATA_FILE)

print("Dataset shape:", df.shape)


# ==========================================================
# 2. Define target
# ==========================================================

TARGET = "target_arrivals"


# ==========================================================
# 3. Remove leakage columns
# ==========================================================

excluded_columns = [
    "target_arrivals",
    "target_queue_length",
    "target_waiting_time",
    "target_congestion_score",
    "target_congestion_level",

    # Current-state variables that would make
    # the model unsuitable for future prediction
    "queue_length",
    "average_waiting_time"
]


X = df.drop(columns=excluded_columns, errors="ignore")
y = df[TARGET]


# ==========================================================
# 4. Keep numerical features only
# ==========================================================

X = X.select_dtypes(include=[np.number])


print("\nFeatures used:")
print(list(X.columns))

print("\nNumber of features:", X.shape[1])


# ==========================================================
# 5. Time-based train/test split
# ==========================================================

split_index = int(len(X) * 0.80)

X_train = X.iloc[:split_index].copy()
X_test = X.iloc[split_index:].copy()

y_train = y.iloc[:split_index].copy()
y_test = y.iloc[split_index:].copy()


print("\nTime-based split:")
print("Training rows:", len(X_train))
print("Testing rows :", len(X_test))


# ==========================================================
# 6. Scale features
# ==========================================================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# ==========================================================
# 7. Build neural network
# ==========================================================

model = tf.keras.Sequential([
    
    tf.keras.layers.Input(shape=(X_train_scaled.shape[1],)),

    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dropout(0.20),

    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dropout(0.20),

    tf.keras.layers.Dense(16, activation="relu"),

    tf.keras.layers.Dense(1)
])


# ==========================================================
# 8. Compile
# ==========================================================

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss="mse",
    metrics=["mae"]
)


model.summary()


# ==========================================================
# 9. Early stopping
# ==========================================================

early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=10,
    restore_best_weights=True
)


# ==========================================================
# 10. Train
# ==========================================================

print("\nStarting training...\n")

history = model.fit(
    X_train_scaled,
    y_train,
    validation_split=0.20,
    epochs=100,
    batch_size=32,
    callbacks=[early_stopping],
    verbose=1
)


# ==========================================================
# 11. Prediction
# ==========================================================

y_pred = model.predict(
    X_test_scaled,
    verbose=0
).flatten()


# ==========================================================
# 12. Evaluation
# ==========================================================

mae = mean_absolute_error(y_test, y_pred)

rmse = np.sqrt(
    mean_squared_error(y_test, y_pred)
)

r2 = r2_score(y_test, y_pred)


print("\n======================================")
print("DEEP LEARNING RESULTS")
print("======================================")

print(f"MAE  : {mae:.4f}")
print(f"RMSE : {rmse:.4f}")
print(f"R2   : {r2:.4f}")


# ==========================================================
# 13. Save model
# ==========================================================

import os

os.makedirs(
    "ai/models/saved_models",
    exist_ok=True
)

model.save(MODEL_FILE)

print("\nModel saved to:")
print(MODEL_FILE)