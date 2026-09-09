import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# 1. LOAD DATA
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "grainflow_features.csv"

df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("GRAINFLOW EXPLORATORY DATA ANALYSIS")
print("=" * 60)

print("\nDataset shape:")
print(df.shape)


# ============================================================
# 2. BASIC INFORMATION
# ============================================================

print("\n--- Dataset Information ---")
print(df.info())


# ============================================================
# 3. CROP ANALYSIS
# ============================================================

print("\n--- Crop Distribution ---")
print(df["crop_type"].value_counts())


# ============================================================
# 4. CENTRE ANALYSIS
# ============================================================

print("\n--- Centre Distribution ---")
print(df["centre_id"].value_counts())


# ============================================================
# 5. CONGESTION ANALYSIS
# ============================================================

print("\n--- Congestion Distribution ---")
print(df["target_congestion_level"].value_counts())


# ============================================================
# 6. TARGET STATISTICS
# ============================================================

target_columns = [
    "target_arrivals",
    "target_queue_length",
    "target_waiting_time",
    "target_congestion_score"
]

print("\n--- Target Statistics ---")
print(df[target_columns].describe())


# ============================================================
# 7. CORRELATION WITH TARGETS
# ============================================================

numeric_df = df.select_dtypes(include="number")

correlation = numeric_df.corr()

print("\n--- Correlation with Target Arrivals ---")
print(
    correlation["target_arrivals"]
    .sort_values(ascending=False)
    .head(10)
)


print("\n--- Correlation with Target Queue Length ---")
print(
    correlation["target_queue_length"]
    .sort_values(ascending=False)
    .head(10)
)


# ============================================================
# 8. ARRIVALS VS QUEUE
# ============================================================

plt.figure(figsize=(8, 5))

plt.scatter(
    df["farmers_arrived"],
    df["queue_length"],
    alpha=0.3
)

plt.xlabel("Farmers Arrived")
plt.ylabel("Queue Length")
plt.title("Farmers Arrived vs Queue Length")

plt.tight_layout()
plt.show()


# ============================================================
# 9. WAITING TIME DISTRIBUTION
# ============================================================

plt.figure(figsize=(8, 5))

plt.hist(
    df["target_waiting_time"],
    bins=30
)

plt.xlabel("Target Waiting Time")
plt.ylabel("Number of Records")
plt.title("Waiting Time Distribution")

plt.tight_layout()
plt.show()


# ============================================================
# 10. CONGESTION DISTRIBUTION
# ============================================================

plt.figure(figsize=(8, 5))

df["target_congestion_level"].value_counts().plot(
    kind="bar"
)

plt.xlabel("Congestion Level")
plt.ylabel("Number of Records")
plt.title("Congestion Level Distribution")

plt.tight_layout()
plt.show()


print("\n" + "=" * 60)
print("EDA COMPLETE")
print("=" * 60)