from pathlib import Path

import duckdb
import pandas as pd
from scipy import stats


SQL_FILE = Path("sql/06_statistical_test_data.sql")

print("=" * 80)
print("PROJECT #3 — STATISTICAL TEST: DELIVERY VS CUSTOMER EXPERIENCE")
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
# Load analysis dataset
# -------------------------------------------------------------------------

df = con.execute("""
    SELECT
        order_id,
        review_score,
        delivery_group
    FROM delivery_review_analysis
    WHERE delivery_group IN ('Late', 'On-time / Early')
""").df()

late = df.loc[
    df["delivery_group"] == "Late",
    "review_score"
].dropna()

ontime = df.loc[
    df["delivery_group"] == "On-time / Early",
    "review_score"
].dropna()

# -------------------------------------------------------------------------
# Descriptive statistics
# -------------------------------------------------------------------------

late_mean = late.mean()
ontime_mean = ontime.mean()

mean_difference = late_mean - ontime_mean

print("\n" + "-" * 80)
print("SAMPLE SIZES")
print("-" * 80)

print(f"Late orders       : {len(late):,}")
print(f"On-time/Early     : {len(ontime):,}")

print("\n" + "-" * 80)
print("MEAN REVIEW SCORE")
print("-" * 80)

print(f"Late              : {late_mean:.4f}")
print(f"On-time / Early   : {ontime_mean:.4f}")
print(f"Difference        : {mean_difference:.4f}")

# -------------------------------------------------------------------------
# Welch's t-test
# -------------------------------------------------------------------------

t_stat, p_value = stats.ttest_ind(
    late,
    ontime,
    equal_var=False
)

print("\n" + "-" * 80)
print("WELCH'S T-TEST")
print("-" * 80)

print(f"t-statistic       : {t_stat:.6f}")
print(f"p-value           : {p_value:.10f}")

# -------------------------------------------------------------------------
# 95% Confidence Interval for difference in means
# -------------------------------------------------------------------------

late_variance = late.var(ddof=1)
ontime_variance = ontime.var(ddof=1)

late_n = len(late)
ontime_n = len(ontime)

standard_error = (
    (late_variance / late_n)
    + (ontime_variance / ontime_n)
) ** 0.5

welch_df = (
    (
        late_variance / late_n
        + ontime_variance / ontime_n
    ) ** 2
    /
    (
        ((late_variance / late_n) ** 2) / (late_n - 1)
        +
        ((ontime_variance / ontime_n) ** 2) / (ontime_n - 1)
    )
)

critical_value = stats.t.ppf(
    0.975,
    welch_df
)

margin_of_error = critical_value * standard_error

ci_lower = mean_difference - margin_of_error
ci_upper = mean_difference + margin_of_error

print("\n" + "-" * 80)
print("95% CONFIDENCE INTERVAL")
print("-" * 80)

print(f"Welch degrees freedom : {welch_df:.2f}")
print(f"Lower bound           : {ci_lower:.4f}")
print(f"Upper bound           : {ci_upper:.4f}")

# -------------------------------------------------------------------------
# Cohen's d
# -------------------------------------------------------------------------

pooled_std = (
    (
        (late_n - 1) * late_variance
        +
        (ontime_n - 1) * ontime_variance
    )
    /
    (late_n + ontime_n - 2)
) ** 0.5

cohens_d = mean_difference / pooled_std

print("\n" + "-" * 80)
print("EFFECT SIZE")
print("-" * 80)

print(f"Cohen's d          : {cohens_d:.4f}")

# -------------------------------------------------------------------------
# Decision
# -------------------------------------------------------------------------

print("\n" + "-" * 80)
print("STATISTICAL INTERPRETATION")
print("-" * 80)

if p_value < 0.05:
    print("Result: Statistically significant difference at alpha = 0.05.")
else:
    print("Result: Not statistically significant at alpha = 0.05.")

print("\nIMPORTANT:")
print("This is observational data.")
print("The statistical test identifies an association,")
print("not proof that late delivery causes lower review scores.")

print("\n" + "=" * 80)
print("STATISTICAL ANALYSIS COMPLETE")
print("=" * 80)

con.close()