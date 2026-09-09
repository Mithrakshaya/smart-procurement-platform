import pandas as pd
from pathlib import Path
from sklearn.preprocessing import LabelEncoder, StandardScaler


# ============================================================
# 1. LOAD DATASET
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "grainflow_historical_data.csv"
OUTPUT_PATH = BASE_DIR / "data" / "grainflow_preprocessed.csv"

df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("GRAINFLOW DATA PREPROCESSING")
print("=" * 60)

print("\nOriginal shape:", df.shape)


# ============================================================
# 2. CONVERT DATE
# ============================================================

df["date"] = pd.to_datetime(df["date"])

df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["day"] = df["date"].dt.day


# ============================================================
# 3. REMOVE ORIGINAL DATE
# ============================================================

df = df.drop(columns=["date"])


# ============================================================
# 4. ENCODE CATEGORICAL FEATURES
# ============================================================

categorical_columns = [
    "day_of_week",
    "centre_id",
    "time_slot",
    "crop_type",
    "weather",
    "harvest_season"
]

label_encoders = {}

for column in categorical_columns:
    encoder = LabelEncoder()
    df[column] = encoder.fit_transform(df[column].astype(str))
    label_encoders[column] = encoder


# ============================================================
# 5. CHECK MISSING VALUES
# ============================================================

print("\nMissing values after preprocessing:")
print(df.isnull().sum().sum())


# ============================================================
# 6. SCALE NUMERICAL FEATURES
# ============================================================

numeric_columns = [
    "total_slots",
    "booked_slots",
    "farmers_arrived",
    "queue_length",
    "average_waiting_time",
    "average_procurement_time",
    "quantity",
    "temperature",
    "rainfall",
    "holiday",
    "previous_day_arrivals",
    "previous_slot_arrivals",
    "year",
    "month",
    "day"
]

scaler = StandardScaler()

df[numeric_columns] = scaler.fit_transform(df[numeric_columns])


# ============================================================
# 7. SAVE PREPROCESSED DATA
# ============================================================

df.to_csv(OUTPUT_PATH, index=False)

print("\nPreprocessed shape:", df.shape)

print("\nSaved to:")
print(OUTPUT_PATH)

print("\nFirst 5 rows:")
print(df.head())

print("\n" + "=" * 60)
print("PREPROCESSING COMPLETE")
print("=" * 60)