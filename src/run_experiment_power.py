from statsmodels.stats.proportion import proportion_effectsize
from statsmodels.stats.power import NormalIndPower

# ============================================================
# PROJECT #3 — STEP 12B
# EXPERIMENT SAMPLE SIZE / POWER ANALYSIS
# ============================================================

print("=" * 80)
print("PROJECT #3 — EXPERIMENT POWER ANALYSIS")
print("=" * 80)

# Observed baseline from Olist experiment population
baseline_rate = 0.127726

# Proposed minimum detectable effect:
# 15% relative reduction in poor-experience rate
relative_reduction = 0.15

treatment_rate = (
    baseline_rate * (1 - relative_reduction)
)

alpha = 0.05
power = 0.80

print("\nEXPERIMENT ASSUMPTIONS")
print("-" * 80)

print(
    "Baseline poor-experience rate: {:.2%}".format(
        baseline_rate
    )
)

print(
    "Target relative reduction: {:.1%}".format(
        relative_reduction
    )
)

print(
    "Expected treatment rate: {:.2%}".format(
        treatment_rate
    )
)

print("Alpha:", alpha)
print("Power:", power)

# Cohen's h for two proportions
effect_size = proportion_effectsize(
    baseline_rate,
    treatment_rate
)

analysis = NormalIndPower()

required_per_group = analysis.solve_power(
    effect_size=effect_size,
    alpha=alpha,
    power=power,
    ratio=1.0,
    alternative="two-sided"
)

required_per_group = int(
    required_per_group + 0.999
)

total_required = (
    required_per_group * 2
)

print("\nSAMPLE SIZE")
print("-" * 80)

print(
    "Required treatment group:",
    required_per_group
)

print(
    "Required control group:",
    required_per_group
)

print(
    "Total required sample:",
    total_required
)

print("\n" + "=" * 80)
print("STEP 12B COMPLETE")
print("=" * 80)