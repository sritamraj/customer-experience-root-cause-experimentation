import duckdb

con = duckdb.connect()

print("=" * 80)
print("PROJECT #3 — DUCKDB DATA CONNECTION TEST")
print("=" * 80)

tables = {
    "customers": "data/raw/olist_customers_dataset.csv",
    "orders": "data/raw/olist_orders_dataset.csv",
    "reviews": "data/raw/olist_order_reviews_dataset.csv",
    "order_items": "data/raw/olist_order_items_dataset.csv",
    "payments": "data/raw/olist_order_payments_dataset.csv",
    "products": "data/raw/olist_products_dataset.csv",
    "sellers": "data/raw/olist_sellers_dataset.csv",
}

for name, path in tables.items():
    query = f"""
        SELECT COUNT(*) AS row_count
        FROM read_csv_auto('{path}')
    """

    result = con.execute(query).fetchone()[0]

    print(f"{name:15s}: {result:,} rows")

print("=" * 80)
print("DUCKDB CONNECTION TEST COMPLETE")
print("=" * 80)

con.close()