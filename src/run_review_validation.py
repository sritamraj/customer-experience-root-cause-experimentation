from pathlib import Path
import duckdb

SQL_FILE = Path("sql/04_review_grain_validation.sql")

con = duckdb.connect()

print("=" * 80)
print("PROJECT #3 — REVIEW GRAIN VALIDATION")
print("=" * 80)

sql = SQL_FILE.read_text(encoding="utf-8")

statements = [
    s.strip()
    for s in sql.split(";")
    if s.strip()
]

for i, statement in enumerate(statements, start=1):

    print("\n" + "-" * 80)
    print(f"QUERY {i}")
    print("-" * 80)

    try:
        result = con.execute(statement)

        try:
            df = result.df()
            print(df.to_string(index=False))
        except Exception:
            print("Statement executed successfully.")

    except Exception as e:

        print("ERROR:")
        print(e)
        break

con.close()

print("\n" + "=" * 80)
print("REVIEW VALIDATION COMPLETE")
print("=" * 80)