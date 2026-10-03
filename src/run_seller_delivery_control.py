import duckdb

con = duckdb.connect()

sql_file = "sql/10_seller_delivery_control.sql"

with open(sql_file, "r", encoding="utf-8") as f:
    sql = f.read()

con.execute(sql)

print("=" * 80)
print("PROJECT #3 — SELLER × DELIVERY CONTROL ANALYSIS")
print("=" * 80)

print("\n" + "-" * 80)
print("VALIDATION")
print("-" * 80)

print(
    con.execute("""
        SELECT
            COUNT(*) AS rows,
            COUNT(DISTINCT seller_id) AS sellers
        FROM seller_delivery_summary
    """).fetchdf().to_string(index=False)
)

print("\n" + "-" * 80)
print("SELLER × DELIVERY RESULTS")
print("-" * 80)

print(
    con.execute("""
        SELECT *
        FROM seller_delivery_summary
        ORDER BY
            seller_id,
            delivery_group
    """).fetchdf().to_string(index=False)
)

print("\n" + "=" * 80)
print("SELLER × DELIVERY CONTROL ANALYSIS COMPLETE")
print("=" * 80)

con.close()