from pathlib import Path

import duckdb
import pandas as pd
from scipy import stats


SQL_FILE = Path("sql/07_poor_experience_test_data.sql")

print("=" * 80)
print("PROJECT #3 — POOR EXPERIENCE ASSOCIATION TEST")
print("=" * 80)

con = duckdb.connect()

# -------------------------------------------------------------------------
# Execute SQL
# -------------------------------------------------------------------------

sql = SQL_FILE.read_text(encoding="utf-8")

for statement in sql.split(";"):
    statement = statement.strip()

    if statement:
        con.execute(statement)

# -------------------------------------------------------------------------
# Load data
# -------------------------------------------------------------------------

df = con.execute("""
    SELECT
        order_id,
        review_score,
        delivery_group,
        poor_experience_flag
    FROM poor_experience_analysis
    WHERE delivery_group IN ('Late', 'On-time / Early')
""").df()

# -------------------------------------------------------------------------
# Contingency table
# -------------------------------------------------------------------------

table = pd.crosstab(
    df["delivery_group"],
    df["poor_experience_flag"]
)

table = table.reindex(
    index=["Late", "On-time / Early"],
    columns=[0, 1],
    fill_value=0
)

table.columns = ["Not Poor Experience", "Poor Experience"]

print("\n" + "-" * 80)
print("CONTINGENCY TABLE")
print("-" * 80)

print(table)

# -------------------------------------------------------------------------
# Rates
# -------------------------------------------------------------------------

late_total = table.loc["Late"].sum()
ontime_total = table.loc["On-time / Early"].sum()

late_poor = table.loc["Late", "Poor Experience"]
ontime_poor = table.loc["On-time / Early", "Poor Experience"]

late_rate = late_poor / late_total
ontime_rate = ontime_poor / ontime_total

print("\n" + "-" * 80)
print("POOR EXPERIENCE RATES")
print("-" * 80)

print(f"Late              : {late_rate:.4%}")
print(f"On-time / Early   : {ontime_rate:.4%}")

# -------------------------------------------------------------------------
# Chi-square test
# -------------------------------------------------------------------------

chi2, p_value, dof, expected = stats.chi2_contingency(table)

print("\n" + "-" * 80)
print("CHI-SQUARE TEST")
print("-" * 80)

print(f"Chi-square statistic : {chi2:.6f}")
print(f"Degrees of freedom   : {dof}")
print(f"p-value              : {p_value:.10f}")

# -------------------------------------------------------------------------
# Cramer's V
# -------------------------------------------------------------------------

n = table.to_numpy().sum()

cramers_v = (chi2 / n) ** 0.5

print("\n" + "-" * 80)
print("EFFECT SIZE")
print("-" * 80)

print(f"Cramer's V           : {cramers_v:.6f}")

# -------------------------------------------------------------------------
# Relative Risk
# -------------------------------------------------------------------------

relative_risk = late_rate / ontime_rate

print("\n" + "-" * 80)
print("RELATIVE RISK")
print("-" * 80)

print(f"Relative Risk        : {relative_risk:.4f}")

# -------------------------------------------------------------------------
# Odds Ratio
# -------------------------------------------------------------------------

a = table.loc["Late", "Poor Experience"]
b = table.loc["Late", "Not Poor Experience"]
c = table.loc["On-time / Early", "Poor Experience"]
d = table.loc["On-time / Early", "Not Poor Experience"]

odds_ratio = (a * d) / (b * c)

print("\n" + "-" * 80)
print("ODDS RATIO")
print("-" * 80)

print(f"Odds Ratio           : {odds_ratio:.4f}")

# -------------------------------------------------------------------------
# Interpretation
# -------------------------------------------------------------------------

print("\n" + "-" * 80)
print("INTERPRETATION")
print("-" * 80)

if p_value < 0.05:
    print("Result: Delivery group and poor experience are statistically associated")
    print("at alpha = 0.05.")
else:
    print("Result: No statistically significant association at alpha = 0.05.")

print("\nIMPORTANT:")
print("This is observational data.")
print("Relative risk and odds ratio describe association, not causation.")

print("\n" + "=" * 80)
print("POOR EXPERIENCE ANALYSIS COMPLETE")
print("=" * 80)

con.close()