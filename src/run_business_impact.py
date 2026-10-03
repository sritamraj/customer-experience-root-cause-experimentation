from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]

population_file = (
    BASE_DIR
    / "reports"
    / "experiment"
    / "experiment_population.csv"
)

simulation_file = (
    BASE_DIR
    / "reports"
    / "experiment"
    / "experiment_simulation_results.csv"
)

# ============================================================
# LOAD DATA
# ============================================================

population = pd.read_csv(population_file)
simulation_raw = pd.read_csv(simulation_file)

# Simulation CSV is stored as:
# metric,value
simulation = dict(
    zip(
        simulation_raw["metric"],
        simulation_raw["value"]
    )
)


# ============================================================
# OBSERVED HISTORICAL BASELINE
# ============================================================

eligible_orders = int(
    population["experiment_population"].iloc[0]
)

baseline_rate = float(
    population["poor_experience_rate"].iloc[0]
)

baseline_poor_orders = (
    eligible_orders * baseline_rate
)


# ============================================================
# EXPERIMENT DESIGN ASSUMPTION
# ============================================================

assumed_relative_reduction = 0.15

assumed_treatment_rate = (
    baseline_rate
    * (1 - assumed_relative_reduction)
)

absolute_rate_reduction = (
    baseline_rate
    - assumed_treatment_rate
)

expected_poor_orders_after = (
    eligible_orders
    * assumed_treatment_rate
)

expected_orders_reduced = (
    baseline_poor_orders
    - expected_poor_orders_after
)


# ============================================================
# SIMULATION RESULTS
# ============================================================

observed_control_rate = float(
    simulation["observed_control_rate"]
)

observed_treatment_rate = float(
    simulation["observed_treatment_rate"]
)

simulated_absolute_difference = float(
    simulation["absolute_difference"]
)

simulated_relative_change = float(
    simulation["relative_change"]
)

simulation_p_value = float(
    simulation["p_value"]
)


# ============================================================
# SCENARIO ANALYSIS
# ============================================================

scenario_volumes = [
    10_000,
    50_000,
    100_000,
    500_000,
    1_000_000
]

scenario_reductions = [
    0.10,
    0.15,
    0.20
]

scenario_rows = []

for volume in scenario_volumes:

    for reduction in scenario_reductions:

        treatment_rate = (
            baseline_rate
            * (1 - reduction)
        )

        expected_reduction = (
            volume
            * (baseline_rate - treatment_rate)
        )

        scenario_rows.append({

            "eligible_orders": volume,

            "assumed_relative_reduction":
                reduction,

            "baseline_poor_experience_rate":
                baseline_rate,

            "assumed_treatment_rate":
                treatment_rate,

            "absolute_rate_reduction":
                baseline_rate - treatment_rate,

            "expected_poor_orders_without_intervention":
                volume * baseline_rate,

            "expected_poor_orders_with_intervention":
                volume * treatment_rate,

            "expected_poor_orders_reduced":
                expected_reduction
        })


scenario_df = pd.DataFrame(
    scenario_rows
)


# ============================================================
# BUSINESS IMPACT SUMMARY
# ============================================================

impact = pd.DataFrame([{

    "historical_eligible_orders":
        eligible_orders,

    "historical_baseline_poor_experience_rate":
        baseline_rate,

    "historical_baseline_poor_experience_orders":
        baseline_poor_orders,

    "assumed_relative_reduction":
        assumed_relative_reduction,

    "assumed_treatment_poor_experience_rate":
        assumed_treatment_rate,

    "assumed_absolute_rate_reduction":
        absolute_rate_reduction,

    "expected_poor_experience_orders_after_intervention":
        expected_poor_orders_after,

    "expected_poor_experience_orders_reduced":
        expected_orders_reduced,

    "simulation_control_rate":
        observed_control_rate,

    "simulation_treatment_rate":
        observed_treatment_rate,

    "simulation_absolute_difference":
        simulated_absolute_difference,

    "simulation_relative_change":
        simulated_relative_change,

    "simulation_p_value":
        simulation_p_value
}])


# ============================================================
# SAVE OUTPUTS
# ============================================================

output_dir = (
    BASE_DIR
    / "reports"
    / "business_impact"
)

output_dir.mkdir(
    parents=True,
    exist_ok=True
)

impact_file = (
    output_dir
    / "business_impact_summary.csv"
)

scenario_file = (
    output_dir
    / "business_impact_scenarios.csv"
)

impact.to_csv(
    impact_file,
    index=False
)

scenario_df.to_csv(
    scenario_file,
    index=False
)


# ============================================================
# PRINT RESULTS
# ============================================================

print()
print("=" * 65)
print("BUSINESS IMPACT ANALYSIS")
print("=" * 65)

print()
print("--- HISTORICAL OBSERVED DATA ---")

print(
    f"Eligible orders: "
    f"{eligible_orders:,}"
)

print(
    f"Baseline poor-experience rate: "
    f"{baseline_rate:.2%}"
)

print(
    f"Baseline poor-experience orders: "
    f"{baseline_poor_orders:,.0f}"
)


print()
print("--- EXPERIMENT DESIGN ASSUMPTION ---")

print(
    f"Assumed relative reduction: "
    f"{assumed_relative_reduction:.0%}"
)

print(
    f"Assumed treatment rate: "
    f"{assumed_treatment_rate:.2%}"
)

print(
    f"Assumed absolute rate reduction: "
    f"{absolute_rate_reduction:.2%}"
)


print()
print("--- EXPECTED BUSINESS IMPACT ---")

print(
    f"Expected poor-experience orders "
    f"after intervention: "
    f"{expected_poor_orders_after:,.0f}"
)

print(
    f"Expected poor-experience orders reduced: "
    f"{expected_orders_reduced:,.0f}"
)


print()
print("--- SIMULATED RANDOMIZED EXPERIMENT ---")

print(
    f"Simulated control rate: "
    f"{observed_control_rate:.2%}"
)

print(
    f"Simulated treatment rate: "
    f"{observed_treatment_rate:.2%}"
)

print(
    f"Simulated absolute difference: "
    f"{simulated_absolute_difference:.2%}"
)

print(
    f"Simulated relative change: "
    f"{simulated_relative_change:.2%}"
)

print(
    f"Simulated p-value: "
    f"{simulation_p_value:.6f}"
)


print()
print("--- SCENARIO ANALYSIS ---")

display_df = scenario_df.copy()

display_df[
    "assumed_relative_reduction"
] = (
    display_df[
        "assumed_relative_reduction"
    ] * 100
)

display_df[
    "assumed_relative_reduction"
] = (
    display_df[
        "assumed_relative_reduction"
    ].map(lambda x: f"{x:.0f}%")
)

print(
    display_df[
        [
            "eligible_orders",
            "assumed_relative_reduction",
            "expected_poor_orders_reduced"
        ]
    ].to_string(index=False)
)


print()
print("--- FILES CREATED ---")

print(impact_file)
print(scenario_file)

print()
print(
    "Business impact analysis completed successfully."
)