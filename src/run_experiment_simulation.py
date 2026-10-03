import os
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency
from statsmodels.stats.proportion import proportions_ztest

# ============================================================
# PROJECT #3 — STEP 12C
# EXPERIMENT ANALYSIS SIMULATION
# ============================================================

print("=" * 80)
print("PROJECT #3 — EXPERIMENT ANALYSIS SIMULATION")
print("=" * 80)

ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

INPUT_FILE = os.path.join(
    ROOT,
    "reports",
    "experiment",
    "experiment_population.csv"
)

OUTPUT_DIR = os.path.join(
    ROOT,
    "reports",
    "experiment"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# ------------------------------------------------------------
# LOAD OBSERVED BASELINE
# ------------------------------------------------------------

population = pd.read_csv(
    INPUT_FILE
)

baseline_rate = float(
    population["poor_experience_rate"].iloc[0]
)

population_size = int(
    population["experiment_population"].iloc[0]
)

print("\nOBSERVED BASELINE")
print("-" * 80)

print(
    "Population:",
    population_size
)

print(
    "Poor-experience rate: {:.2%}".format(
        baseline_rate
    )
)

# ------------------------------------------------------------
# SIMULATED RANDOMIZED EXPERIMENT
# ------------------------------------------------------------

np.random.seed(42)

n_per_group = 4449

control_rate = baseline_rate

# Design assumption:
# 15% relative reduction
treatment_rate = (
    baseline_rate * 0.85
)

control = np.random.binomial(
    1,
    control_rate,
    n_per_group
)

treatment = np.random.binomial(
    1,
    treatment_rate,
    n_per_group
)

control_poor = control.sum()
treatment_poor = treatment.sum()

control_observed = (
    control_poor / n_per_group
)

treatment_observed = (
    treatment_poor / n_per_group
)

# ------------------------------------------------------------
# EFFECT
# ------------------------------------------------------------

absolute_difference = (
    treatment_observed
    - control_observed
)

relative_change = (
    absolute_difference
    / control_observed
)

# ------------------------------------------------------------
# TWO-PROPORTION TEST
# ------------------------------------------------------------

counts = np.array([
    treatment_poor,
    control_poor
])

sample_sizes = np.array([
    n_per_group,
    n_per_group
])

z_stat, p_value = proportions_ztest(
    counts,
    sample_sizes
)

# ------------------------------------------------------------
# CONTINGENCY TABLE
# ------------------------------------------------------------

table = np.array(
    [
        [
            treatment_poor,
            n_per_group - treatment_poor
        ],
        [
            control_poor,
            n_per_group - control_poor
        ]
    ]
)

chi2, chi_p, dof, expected = (
    chi2_contingency(table)
)

# ------------------------------------------------------------
# OUTPUT
# ------------------------------------------------------------

print("\nSIMULATED EXPERIMENT")
print("-" * 80)

print(
    "Control poor-experience rate: {:.2%}".format(
        control_observed
    )
)

print(
    "Treatment poor-experience rate: {:.2%}".format(
        treatment_observed
    )
)

print(
    "Absolute difference: {:.2%}".format(
        absolute_difference
    )
)

print(
    "Relative change: {:.2%}".format(
        relative_change
    )
)

print(
    "Two-proportion z-test p-value: {:.6f}".format(
        p_value
    )
)

print(
    "Chi-square p-value: {:.6f}".format(
        chi_p
    )
)

print("\nINTERPRETATION")
print("-" * 80)

print(
    "This is a simulated randomized experiment, "
    "not an observed Olist A/B test."
)

print(
    "The treatment effect is generated from the "
    "15% relative-reduction design assumption."
)

# ------------------------------------------------------------
# SAVE
# ------------------------------------------------------------

results = pd.DataFrame(
    {
        "metric": [
            "population",
            "n_per_group",
            "baseline_rate",
            "design_treatment_rate",
            "observed_control_rate",
            "observed_treatment_rate",
            "absolute_difference",
            "relative_change",
            "z_statistic",
            "p_value"
        ],
        "value": [
            population_size,
            n_per_group,
            baseline_rate,
            treatment_rate,
            control_observed,
            treatment_observed,
            absolute_difference,
            relative_change,
            z_stat,
            p_value
        ]
    }
)

output_file = os.path.join(
    OUTPUT_DIR,
    "experiment_simulation_results.csv"
)

results.to_csv(
    output_file,
    index=False
)

print("\nFILE SAVED")
print("-" * 80)

print(
    "reports/experiment/"
    "experiment_simulation_results.csv"
)

print("\n" + "=" * 80)
print("STEP 12C COMPLETE")
print("=" * 80)