from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/raw")

files = sorted(DATA_DIR.glob("*.csv"))

print("=" * 80)
print("PROJECT #3 — DATASET INSPECTION")
print("=" * 80)

print(f"\nCSV files found: {len(files)}\n")

for file in files:
    try:
        df = pd.read_csv(file)

        print("-" * 80)
        print(f"FILE: {file.name}")
        print(f"ROWS: {len(df):,}")
        print(f"COLUMNS: {len(df.columns)}")
        print(f"SHAPE: {df.shape}")

        print("\nCOLUMNS:")
        for column in df.columns:
            print(f"  - {column}")

        print("\nMISSING VALUES:")
        missing = df.isna().sum()
        missing = missing[missing > 0].sort_values(ascending=False)

        if len(missing) == 0:
            print("  None")
        else:
            print(missing)

        print(f"\nDUPLICATE ROWS: {df.duplicated().sum():,}")

    except Exception as e:
        print(f"ERROR reading {file.name}: {e}")

print("\n" + "=" * 80)
print("INSPECTION COMPLETE")
print("=" * 80)