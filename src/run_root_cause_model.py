import os
import warnings

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

warnings.filterwarnings("ignore")

# ============================================================
# PROJECT #3 — MULTIVARIATE ROOT-CAUSE MODEL
# Sparse L2 Logistic Regression
# ============================================================

print("=" * 80)
print("PROJECT #3 — MULTIVARIATE ROOT-CAUSE MODEL")
print("Sparse L2 Logistic Regression")
print("=" * 80)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

print("\nLOADING DATA")

orders = pd.read_csv(
    os.path.join(RAW, "olist_orders_dataset.csv")
)

reviews = pd.read_csv(
    os.path.join(RAW, "olist_order_reviews_dataset.csv")
)

items = pd.read_csv(
    os.path.join(RAW, "olist_order_items_dataset.csv")
)

products = pd.read_csv(
    os.path.join(RAW, "olist_products_dataset.csv")
)

# ------------------------------------------------------------
# REVIEW: ONE ROW PER ORDER
# ------------------------------------------------------------

review_one = (
    reviews
    .groupby("order_id", as_index=False)
    .agg(
        review_score=("review_score", "mean")
    )
)

review_one["poor_experience"] = (
    review_one["review_score"] <= 2
).astype(int)

# ------------------------------------------------------------
# DELIVERY STATUS
# ------------------------------------------------------------

orders["order_delivered_customer_date"] = pd.to_datetime(
    orders["order_delivered_customer_date"],
    errors="coerce"
)

orders["order_estimated_delivery_date"] = pd.to_datetime(
    orders["order_estimated_delivery_date"],
    errors="coerce"
)

orders["late_delivery"] = (
    orders["order_delivered_customer_date"]
    > orders["order_estimated_delivery_date"]
).astype(int)

# ------------------------------------------------------------
# ORDER VALUE
# ------------------------------------------------------------

order_value = (
    items
    .groupby("order_id", as_index=False)
    .agg(
        order_value=("price", "sum")
    )
)

# ------------------------------------------------------------
# REPRESENTATIVE SELLER
# Highest-value seller per order
# ------------------------------------------------------------

seller_value = (
    items
    .groupby(
        ["order_id", "seller_id"],
        as_index=False
    )
    .agg(
        seller_value=("price", "sum")
    )
)

seller_value["seller_rank"] = (
    seller_value
    .groupby("order_id")["seller_value"]
    .rank(
        method="first",
        ascending=False
    )
)

primary_seller = seller_value[
    seller_value["seller_rank"] == 1
][
    ["order_id", "seller_id"]
]

# ------------------------------------------------------------
# REPRESENTATIVE PRODUCT CATEGORY
# Highest-value category per order
# ------------------------------------------------------------

items_products = items.merge(
    products[
        [
            "product_id",
            "product_category_name"
        ]
    ],
    on="product_id",
    how="left"
)

category_value = (
    items_products
    .groupby(
        [
            "order_id",
            "product_category_name"
        ],
        dropna=False,
        as_index=False
    )
    .agg(
        category_value=("price", "sum")
    )
)

category_value["category_rank"] = (
    category_value
    .groupby("order_id")["category_value"]
    .rank(
        method="first",
        ascending=False
    )
)

primary_category = category_value[
    category_value["category_rank"] == 1
][
    [
        "order_id",
        "product_category_name"
    ]
].copy()

primary_category["product_category_name"] = (
    primary_category["product_category_name"]
    .fillna("unknown")
)

# ------------------------------------------------------------
# BUILD MODEL DATASET
# ------------------------------------------------------------

df = (
    orders[
        [
            "order_id",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
            "late_delivery"
        ]
    ]
    .merge(
        review_one[
            [
                "order_id",
                "poor_experience"
            ]
        ],
        on="order_id",
        how="inner"
    )
    .merge(
        order_value,
        on="order_id",
        how="left"
    )
    .merge(
        primary_seller,
        on="order_id",
        how="left"
    )
    .merge(
        primary_category,
        on="order_id",
        how="left"
    )
)

# Only orders with valid delivered + estimated dates
df = df[
    df["order_delivered_customer_date"].notna()
    & df["order_estimated_delivery_date"].notna()
].copy()

df["seller_id"] = (
    df["seller_id"]
    .fillna("unknown")
    .astype(str)
)

df["product_category_name"] = (
    df["product_category_name"]
    .fillna("unknown")
    .astype(str)
)

df["log_order_value"] = np.log1p(
    df["order_value"].clip(lower=0)
)

# Group low-frequency categories
category_counts = (
    df["product_category_name"]
    .value_counts()
)

valid_categories = category_counts[
    category_counts >= 300
].index

df["category_group"] = np.where(
    df["product_category_name"].isin(valid_categories),
    df["product_category_name"],
    "other"
)

# ------------------------------------------------------------
# VALIDATION
# ------------------------------------------------------------

print("\nDATASET")
print("-" * 80)

print("Rows:", len(df))
print("Columns:", len(df.columns))

print(
    "Poor experience rate: {:.2f}%".format(
        df["poor_experience"].mean() * 100
    )
)

print(
    "Late delivery rate: {:.2f}%".format(
        df["late_delivery"].mean() * 100
    )
)

print(
    "Unique sellers:",
    df["seller_id"].nunique()
)

print(
    "Category groups:",
    df["category_group"].nunique()
)

# ------------------------------------------------------------
# FEATURES
# ------------------------------------------------------------

X = df[
    [
        "late_delivery",
        "log_order_value",
        "seller_id",
        "category_group"
    ]
].copy()

y = df["poor_experience"].astype(int)

# ------------------------------------------------------------
# TRAIN / TEST
# ------------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTRAIN / TEST")
print("-" * 80)

print("Train rows:", len(X_train))
print("Test rows:", len(X_test))

# ------------------------------------------------------------
# PREPROCESSING
# ------------------------------------------------------------

numeric_features = [
    "late_delivery",
    "log_order_value"
]

categorical_features = [
    "seller_id",
    "category_group"
]

numeric_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="median")
        ),
        (
            "scaler",
            StandardScaler()
        )
    ]
)

categorical_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="most_frequent")
        ),
        (
            "onehot",
            OneHotEncoder(
                handle_unknown="ignore",
                min_frequency=20
            )
        )
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        (
            "numeric",
            numeric_pipeline,
            numeric_features
        ),
        (
            "categorical",
            categorical_pipeline,
            categorical_features
        )
    ]
)

# ------------------------------------------------------------
# MODEL
# ------------------------------------------------------------

model = LogisticRegression(
    penalty="l2",
    C=1.0,
    solver="liblinear",
    max_iter=1000,
    class_weight="balanced",
    random_state=42
)

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)

print("\nTRAINING MODEL")
print("-" * 80)

pipeline.fit(
    X_train,
    y_train
)

print("Model training completed.")

# ------------------------------------------------------------
# PREDICTIONS
# ------------------------------------------------------------

y_pred = pipeline.predict(X_test)

y_prob = pipeline.predict_proba(
    X_test
)[:, 1]

# ------------------------------------------------------------
# PERFORMANCE
# ------------------------------------------------------------

roc_auc = roc_auc_score(
    y_test,
    y_prob
)

pr_auc = average_precision_score(
    y_test,
    y_prob
)

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("\nMODEL PERFORMANCE")
print("-" * 80)

print(
    "Accuracy: {:.4f}".format(
        accuracy
    )
)

print(
    "ROC-AUC:  {:.4f}".format(
        roc_auc
    )
)

print(
    "PR-AUC:   {:.4f}".format(
        pr_auc
    )
)

print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        digits=4
    )
)

# ------------------------------------------------------------
# COEFFICIENTS
# ------------------------------------------------------------

feature_names = (
    pipeline
    .named_steps["preprocessor"]
    .get_feature_names_out()
)

coefficients = (
    pipeline
    .named_steps["model"]
    .coef_[0]
)

effects = pd.DataFrame(
    {
        "feature": feature_names,
        "coefficient": coefficients
    }
)

effects["odds_ratio"] = np.exp(
    effects["coefficient"]
)

# ------------------------------------------------------------
# LATE DELIVERY EFFECT
# ------------------------------------------------------------

late_effect = effects[
    effects["feature"].str.contains(
        "late_delivery",
        regex=False
    )
]

print("\nLATE DELIVERY EFFECT")
print("-" * 80)

print(
    late_effect.to_string(
        index=False
    )
)

# ------------------------------------------------------------
# TOP POSITIVE ASSOCIATIONS
# ------------------------------------------------------------

print(
    "\nTOP POSITIVE ASSOCIATIONS WITH POOR EXPERIENCE"
)

print("-" * 80)

print(
    effects
    .sort_values(
        "coefficient",
        ascending=False
    )
    .head(20)
    .to_string(index=False)
)

# ------------------------------------------------------------
# TOP NEGATIVE ASSOCIATIONS
# ------------------------------------------------------------

print(
    "\nTOP NEGATIVE ASSOCIATIONS WITH POOR EXPERIENCE"
)

print("-" * 80)

print(
    effects
    .sort_values(
        "coefficient",
        ascending=True
    )
    .head(20)
    .to_string(index=False)
)

# ------------------------------------------------------------
# SAVE RESULTS
# ------------------------------------------------------------

output_dir = os.path.join(
    ROOT,
    "reports",
    "model"
)

os.makedirs(
    output_dir,
    exist_ok=True
)

effects.to_csv(
    os.path.join(
        output_dir,
        "root_cause_feature_effects.csv"
    ),
    index=False
)

metrics = pd.DataFrame(
    {
        "metric": [
            "rows",
            "train_rows",
            "test_rows",
            "poor_experience_rate",
            "late_delivery_rate",
            "accuracy",
            "roc_auc",
            "pr_auc"
        ],
        "value": [
            len(df),
            len(X_train),
            len(X_test),
            y.mean(),
            df["late_delivery"].mean(),
            accuracy,
            roc_auc,
            pr_auc
        ]
    }
)

metrics.to_csv(
    os.path.join(
        output_dir,
        "root_cause_model_metrics.csv"
    ),
    index=False
)

print("\nFILES SAVED")
print("-" * 80)

print(
    "reports/model/root_cause_feature_effects.csv"
)

print(
    "reports/model/root_cause_model_metrics.csv"
)

print("\n" + "=" * 80)
print("STEP 11 COMPLETE")
print("=" * 80)