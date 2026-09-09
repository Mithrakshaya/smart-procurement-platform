import pandas as pd
from pathlib import Path


# ============================================================
# 1. LOAD FEATURE DATASET
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "grainflow_features.csv"

df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("GRAINFLOW DATA LEAKAGE CHECK")
print("=" * 60)

print("\nDataset shape:", df.shape)


# ============================================================
# 2. TARGET COLUMNS
# ============================================================

target_columns = [
    "target_arrivals",
    "target_queue_length",
    "target_waiting_time",
    "target_congestion_score",
    "target_congestion_level"
]


# ============================================================
# 3. CHECK TARGET-TO-FEATURE CORRELATIONS
# ============================================================

numeric_df = df.select_dtypes(include="number")

for target in target_columns[:-1]:

    print("\n" + "-" * 60)
    print(f"Correlation with {target}")
    print("-" * 60)

    correlations = (
        numeric_df.corr()[target]
        .drop(target)
        .abs()
        .sort_values(ascending=False)
    )

    print(correlations.head(10))


# ============================================================
# 4. CHECK DIRECTLY RELATED FEATURES
# ============================================================

suspicious_features = [
    "farmers_arrived",
    "queue_length",
    "average_waiting_time",
    "target_arrivals",
    "target_queue_length",
    "target_waiting_time",
    "target_congestion_score"
]

print("\n" + "-" * 60)
print("Potentially suspicious columns")
print("-" * 60)

for column in suspicious_features:

    if column in df.columns:
        print(f"{column}: PRESENT")


# ============================================================
# 5. FINAL MESSAGE
# ============================================================

print("\n" + "=" * 60)
print("LEAKAGE CHECK COMPLETE")
print("=" * 60)