from pathlib import Path
import duckdb

SQL_FILE = Path("sql/02_customer_experience_base.sql")

con = duckdb.connect()

print("=" * 80)
print("PROJECT #3 — CUSTOMER EXPERIENCE BASE DATASET")
print("=" * 80)

sql = SQL_FILE.read_text(encoding="utf-8")

try:
    results = con.execute(sql)

    print("\nSQL EXECUTION SUCCESSFUL.\n")

    print("=" * 80)
    print("FINAL QUERY RESULT")
    print("=" * 80)

    try:
        print(results.df().to_string(index=False))
    except Exception:
        print("SQL completed successfully.")

except Exception as e:

    print("\nSQL EXECUTION FAILED")
    print("-" * 80)
    print(e)

finally:
    con.close()

print("\n" + "=" * 80)
print("COMPLETE")
print("=" * 80)