from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]


def test_experiment_population_exists():
    path = (
        BASE_DIR
        / "reports"
        / "experiment"
        / "experiment_population.csv"
    )

    assert path.exists()


def test_experiment_simulation_exists():
    path = (
        BASE_DIR
        / "reports"
        / "experiment"
        / "experiment_simulation_results.csv"
    )

    assert path.exists()


def test_business_impact_exists():
    path = (
        BASE_DIR
        / "reports"
        / "business_impact"
        / "business_impact_summary.csv"
    )

    assert path.exists()


def test_experiment_population_values():

    path = (
        BASE_DIR
        / "reports"
        / "experiment"
        / "experiment_population.csv"
    )

    df = pd.read_csv(path)

    population = int(
        df["experiment_population"].iloc[0]
    )

    poor_rate = float(
        df["poor_experience_rate"].iloc[0]
    )

    assert population > 0
    assert 0 < poor_rate < 1


def test_simulation_schema():

    path = (
        BASE_DIR
        / "reports"
        / "experiment"
        / "experiment_simulation_results.csv"
    )

    df = pd.read_csv(path)

    assert "metric" in df.columns
    assert "value" in df.columns

    metrics = set(df["metric"])

    required_metrics = {
        "population",
        "n_per_group",
        "baseline_rate",
        "design_treatment_rate",
        "observed_control_rate",
        "observed_treatment_rate",
        "absolute_difference",
        "relative_change",
        "p_value"
    }

    assert required_metrics.issubset(metrics)


def test_business_impact_values():

    path = (
        BASE_DIR
        / "reports"
        / "business_impact"
        / "business_impact_summary.csv"
    )

    df = pd.read_csv(path)

    baseline = float(
        df[
            "historical_baseline_poor_experience_rate"
        ].iloc[0]
    )

    treatment = float(
        df[
            "assumed_treatment_poor_experience_rate"
        ].iloc[0]
    )

    reduction = float(
        df[
            "expected_poor_experience_orders_reduced"
        ].iloc[0]
    )

    assert 0 < baseline < 1
    assert 0 < treatment < 1
    assert reduction > 0