from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parents[1]
FIG_DIR = BASE_DIR / "reports" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# 1. Delivery status vs poor experience
# ---------------------------------------------------------
delivery_data = pd.DataFrame({
    "Delivery Status": ["On-time / Early", "Late"],
    "Poor Experience Rate": [9.1915, 53.9807],
})

plt.figure(figsize=(8, 5))
plt.bar(
    delivery_data["Delivery Status"],
    delivery_data["Poor Experience Rate"],
)
plt.ylabel("Poor Experience Rate (%)")
plt.xlabel("Delivery Status")
plt.title("Poor Experience Rate by Delivery Status")
plt.ylim(0, 60)
plt.tight_layout()
plt.savefig(FIG_DIR / "delivery_vs_poor_experience.png", dpi=200)
plt.close()


# ---------------------------------------------------------
# 2. Review score: late vs on-time
# ---------------------------------------------------------
review_data = pd.DataFrame({
    "Delivery Status": ["On-time / Early", "Late"],
    "Average Review Score": [4.2942, 2.5666],
})

plt.figure(figsize=(8, 5))
plt.bar(
    review_data["Delivery Status"],
    review_data["Average Review Score"],
)
plt.ylabel("Average Review Score")
plt.xlabel("Delivery Status")
plt.title("Average Review Score: Late vs On-time / Early")
plt.ylim(0, 5)
plt.tight_layout()
plt.savefig(FIG_DIR / "review_score_late_vs_ontime.png", dpi=200)
plt.close()


# ---------------------------------------------------------
# 3. Root-cause modeled odds ratio
# ---------------------------------------------------------
odds_data = pd.DataFrame({
    "Feature": ["Late Delivery"],
    "Odds Ratio": [2.030036],
})

plt.figure(figsize=(7, 5))
plt.bar(
    odds_data["Feature"],
    odds_data["Odds Ratio"],
)
plt.axhline(1.0, linestyle="--")
plt.ylabel("Modeled Odds Ratio")
plt.xlabel("Feature")
plt.title("Modeled Association with Poor Experience")
plt.ylim(0, 2.5)
plt.tight_layout()
plt.savefig(FIG_DIR / "root_cause_odds_ratios.png", dpi=200)
plt.close()


# ---------------------------------------------------------
# 4. Experiment framework
# ---------------------------------------------------------
steps = [
    "Eligible\nCustomers",
    "Randomize",
    "Control",
    "Treatment",
    "Measure\nPoor CX",
    "Estimate\nEffect",
]

fig, ax = plt.subplots(figsize=(12, 3))

for i, step in enumerate(steps):
    ax.text(
        i,
        0.5,
        step,
        ha="center",
        va="center",
        fontsize=11,
        bbox=dict(boxstyle="round,pad=0.6", fill=False),
    )

    if i < len(steps) - 1:
        ax.annotate(
            "",
            xy=(i + 0.75, 0.5),
            xytext=(i + 0.25, 0.5),
            arrowprops=dict(arrowstyle="->"),
        )

ax.set_xlim(-0.5, len(steps) - 0.5)
ax.set_ylim(0, 1)
ax.axis("off")
ax.set_title("Proposed Randomized Experiment Framework")

plt.tight_layout()
plt.savefig(FIG_DIR / "experiment_framework.png", dpi=200)
plt.close()


print("Created:")
for file in sorted(FIG_DIR.glob("*.png")):
    print(file)