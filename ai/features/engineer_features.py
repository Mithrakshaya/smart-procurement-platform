import pandas as pd
import numpy as np

INPUT_FILE = "ai/data/grainflow_preprocessed.csv"
OUTPUT_FILE = "ai/data/grainflow_features.csv"

print("Loading preprocessed dataset...")

df = pd.read_csv(INPUT_FILE)

print("Input shape:", df.shape)

# --------------------------------------------------
# Safe denominator
# --------------------------------------------------

def safe_divide(a, b):
    return a / np.maximum(np.abs(b), 1.0)


# --------------------------------------------------
# Feature Engineering
# --------------------------------------------------

# Booking pressure
df["booking_ratio"] = safe_divide(
    df["booked_slots"],
    df["total_slots"]
)

# Queue pressure per available slot
df["queue_per_slot"] = safe_divide(
    df["queue_length"],
    df["total_slots"]
)

# Arrival pressure
df["arrival_pressure"] = safe_divide(
    df["farmers_arrived"],
    df["total_slots"]
)

# Procurement load
df["procurement_load"] = (
    df["farmers_arrived"] *
    df["average_procurement_time"]
)

# Historical arrival trend
df["historical_arrival_trend"] = (
    0.5 * df["previous_day_arrivals"] +
    0.5 * df["previous_slot_arrivals"]
)

# Weather impact
df["weather_impact"] = (
    df["rainfall"] * 0.5 +
    df["temperature"] * 0.2
)

# Queue pressure
df["queue_pressure"] = (
    0.6 * df["queue_length"] +
    0.4 * df["farmers_arrived"]
)


# --------------------------------------------------
# Clean infinite values
# --------------------------------------------------

df.replace([np.inf, -np.inf], np.nan, inplace=True)

df.fillna(0, inplace=True)


# --------------------------------------------------
# Save
# --------------------------------------------------

df.to_csv(OUTPUT_FILE, index=False)

print("\nFEATURE ENGINEERING COMPLETED")

print("Input shape :", (7000, 26))
print("Output shape:", df.shape)

print("\nNew features:")
print([
    "booking_ratio",
    "queue_per_slot",
    "arrival_pressure",
    "procurement_load",
    "historical_arrival_trend",
    "weather_impact",
    "queue_pressure"
])

print("\nFeature statistics:")

print(
    df[
        [
            "booking_ratio",
            "queue_per_slot",
            "arrival_pressure",
            "procurement_load",
            "historical_arrival_trend",
            "weather_impact",
            "queue_pressure"
        ]
    ].describe().T[
        ["mean", "std", "min", "max"]
    ]
)

print("\nSaved to:")
print(OUTPUT_FILE)