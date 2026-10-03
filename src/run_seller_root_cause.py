from pathlib import Path

import duckdb


SQL_FILE = Path("sql/09_seller_root_cause.sql")

print("=" * 80)
print("PROJECT #3 — SELLER ROOT-CAUSE ANALYSIS")
print("=" * 80)

con = duckdb.connect()

sql = SQL_FILE.read_text(encoding="utf-8")

statements = [
    statement.strip()
    for statement in sql.split(";")
    if statement.strip()
]

for i, statement in enumerate(statements, start=1):

    result = con.execute(statement)

    try:
        df = result.df()

        if not df.empty:
            print("\n" + "-" * 80)
            print(f"RESULT {i}")
            print("-" * 80)

            print(df.to_string(index=False))

    except Exception:
        pass

print("\n" + "=" * 80)
print("SELLER ROOT-CAUSE ANALYSIS COMPLETE")
print("=" * 80)

con.close()