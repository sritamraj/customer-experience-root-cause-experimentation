import duckdb
import os

ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DB_PATH = os.path.join(
    ROOT,
    "data",
    "project3_experiment.duckdb"
)

SQL_PATH = os.path.join(
    ROOT,
    "sql",
    "12_experiment_design.sql"
)

print("=" * 80)
print("PROJECT #3 — STEP 12 EXPERIMENT DESIGN")
print("=" * 80)

con = duckdb.connect(DB_PATH)

with open(SQL_PATH, "r", encoding="utf-8") as f:
    sql = f.read()

result = con.execute(sql).fetchdf()

print("\nEXPERIMENT POPULATION")
print("-" * 80)

print(result.to_string(index=False))

output_dir = os.path.join(
    ROOT,
    "reports",
    "experiment"
)

os.makedirs(
    output_dir,
    exist_ok=True
)

output_file = os.path.join(
    output_dir,
    "experiment_population.csv"
)

result.to_csv(
    output_file,
    index=False
)

print("\nFILE SAVED")
print("-" * 80)
print(
    "reports/experiment/experiment_population.csv"
)

con.close()

print("\n" + "=" * 80)
print("STEP 12A COMPLETE")
print("=" * 80)