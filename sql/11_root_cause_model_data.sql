-- ============================================================
-- PROJECT #3 — MULTIVARIATE ROOT-CAUSE MODEL DATA
-- ============================================================

DROP VIEW IF EXISTS root_cause_model_data;

CREATE VIEW root_cause_model_data AS

WITH

orders AS (
    SELECT
        order_id,
        order_delivered_customer_date,
        order_estimated_delivery_date
    FROM read_csv_auto(
        'data/raw/olist_orders_dataset.csv'
    )
),

reviews AS (
    SELECT
        order_id,
        AVG(review_score) AS review_score
    FROM read_csv_auto(
        'data/raw/olist_order_reviews_dataset.csv'
    )
    GROUP BY order_id
),

order_items AS (
    SELECT
        order_id,
        seller_id,
        product_id,
        price,
        freight_value
    FROM read_csv_auto(
        'data/raw/olist_order_items_dataset.csv'
    )
),

products AS (
    SELECT
        product_id,
        product_category_name
    FROM read_csv_auto(
        'data/raw/olist_products_dataset.csv'
    )
),

-- ------------------------------------------------------------
-- Order-level seller value
-- ------------------------------------------------------------

seller_value AS (
    SELECT
        order_id,
        seller_id,
        SUM(
            COALESCE(price, 0)
            + COALESCE(freight_value, 0)
        ) AS seller_value
    FROM order_items
    GROUP BY
        order_id,
        seller_id
),

primary_seller AS (
    SELECT
        order_id,
        seller_id
    FROM (
        SELECT
            order_id,
            seller_id,
            seller_value,

            ROW_NUMBER() OVER (
                PARTITION BY order_id
                ORDER BY
                    seller_value DESC,
                    seller_id
            ) AS rn

        FROM seller_value
    )
    WHERE rn = 1
),

-- ------------------------------------------------------------
-- Order-level category
-- Highest-value category represents the order
-- ------------------------------------------------------------

category_value AS (
    SELECT
        oi.order_id,
        p.product_category_name,
        SUM(
            COALESCE(oi.price, 0)
            + COALESCE(oi.freight_value, 0)
        ) AS category_value
    FROM order_items oi

    LEFT JOIN products p
        ON oi.product_id = p.product_id

    GROUP BY
        oi.order_id,
        p.product_category_name
),

primary_category AS (
    SELECT
        order_id,
        COALESCE(
            product_category_name,
            'unknown'
        ) AS product_category_name
    FROM (
        SELECT
            order_id,
            product_category_name,
            category_value,

            ROW_NUMBER() OVER (
                PARTITION BY order_id
                ORDER BY
                    category_value DESC,
                    product_category_name
            ) AS rn

        FROM category_value
    )
    WHERE rn = 1
),

-- ------------------------------------------------------------
-- Order value
-- ------------------------------------------------------------

order_value AS (
    SELECT
        order_id,

        SUM(
            COALESCE(price, 0)
            + COALESCE(freight_value, 0)
        ) AS order_value

    FROM order_items

    GROUP BY order_id
)

-- ------------------------------------------------------------
-- FINAL MODEL DATASET
-- ------------------------------------------------------------

SELECT

    o.order_id,

    r.review_score,

    CASE
        WHEN r.review_score <= 2
        THEN 1
        ELSE 0
    END AS poor_experience,

    CASE
        WHEN
            o.order_delivered_customer_date
                > o.order_estimated_delivery_date
        THEN 1
        ELSE 0
    END AS late_delivery,

    ps.seller_id,

    pc.product_category_name,

    ov.order_value

FROM orders o

INNER JOIN reviews r
    ON o.order_id = r.order_id

INNER JOIN primary_seller ps
    ON o.order_id = ps.order_id

INNER JOIN primary_category pc
    ON o.order_id = pc.order_id

INNER JOIN order_value ov
    ON o.order_id = ov.order_id

WHERE
    o.order_delivered_customer_date IS NOT NULL
    AND o.order_estimated_delivery_date IS NOT NULL;