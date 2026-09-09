import pandas as pd
from pathlib import Path

print("Starting dataset inspection...")

# Get the folder where this Python file is located
data_folder = Path(__file__).resolve().parent

# Dataset file
dataset_path = data_folder / "grainflow_historical_data.csv"

print("Looking for dataset at:")
print(dataset_path)

# Check whether file exists
if not dataset_path.exists():
    print("\nERROR: Dataset file not found!")
    raise SystemExit

# Check file size
print(f"\nFile size: {dataset_path.stat().st_size} bytes")

if dataset_path.stat().st_size == 0:
    print("\nERROR: Dataset file is empty!")
    raise SystemExit

# Load dataset
df = pd.read_csv(dataset_path)

print("\n" + "=" * 60)
print("DATASET INSPECTION")
print("=" * 60)

print("\n1. Dataset Shape:")
print(df.shape)

print("\n2. Columns:")
print(df.columns.tolist())

print("\n3. Data Types:")
print(df.dtypes)

print("\n4. Missing Values:")
print(df.isnull().sum())

print("\n5. Duplicate Rows:")
print(df.duplicated().sum())

print("\n6. First 5 Rows:")
print(df.head())

print("\n7. Numerical Statistics:")
print(df.describe())

print("\n8. Congestion Levels:")
print(df["target_congestion_level"].value_counts())

print("\n" + "=" * 60)
print("INSPECTION COMPLETE")
print("=" * 60)