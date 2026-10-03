-- STEP 8A-FIX
-- PRODUCT CATEGORY ROOT-CAUSE ANALYSIS
-- Grain: ONE ROW PER ORDER
--
-- Representative category:
-- The category contributing the highest item value
-- within each order.

CREATE OR REPLACE TABLE orders AS
SELECT *
FROM read_csv_auto('data/raw/olist_orders_dataset.csv');

CREATE OR REPLACE TABLE reviews AS
SELECT *
FROM read_csv_auto('data/raw/olist_order_reviews_dataset.csv');

CREATE OR REPLACE TABLE order_items AS
SELECT *
FROM read_csv_auto('data/raw/olist_order_items_dataset.csv');

CREATE OR REPLACE TABLE products AS
SELECT *
FROM read_csv_auto('data/raw/olist_products_dataset.csv');

CREATE OR REPLACE TABLE category_translation AS
SELECT *
FROM read_csv_auto(
    'data/raw/product_category_name_translation.csv'
);

-- ------------------------------------------------------------
-- ONE REVIEW SCORE PER ORDER
-- ------------------------------------------------------------

CREATE OR REPLACE TABLE review_one_per_order AS
SELECT
    order_id,
    AVG(review_score) AS review_score
FROM reviews
GROUP BY order_id;

-- ------------------------------------------------------------
-- CATEGORY VALUE PER ORDER
-- ------------------------------------------------------------

CREATE OR REPLACE TABLE order_category_value AS
SELECT
    oi.order_id,

    COALESCE(
        ct.product_category_name_english,
        p.product_category_name,
        'unknown'
    ) AS product_category,

    SUM(
        COALESCE(oi.price, 0)
        + COALESCE(oi.freight_value, 0)
    ) AS category_order_value

FROM order_items oi

LEFT JOIN products p
    ON oi.product_id = p.product_id

LEFT JOIN category_translation ct
    ON p.product_category_name =
       ct.product_category_name

GROUP BY
    oi.order_id,
    COALESCE(
        ct.product_category_name_english,
        p.product_category_name,
        'unknown'
    );

-- ------------------------------------------------------------
-- SELECT ONE REPRESENTATIVE CATEGORY PER ORDER
-- ------------------------------------------------------------

CREATE OR REPLACE TABLE primary_order_category AS

SELECT
    order_id,
    product_category,
    category_order_value

FROM (
    SELECT
        order_id,
        product_category,
        category_order_value,

        ROW_NUMBER() OVER (
            PARTITION BY order_id
            ORDER BY
                category_order_value DESC,
                product_category
        ) AS category_rank

    FROM order_category_value
)

WHERE category_rank = 1;

-- ------------------------------------------------------------
-- BUILD FINAL ORDER-LEVEL ANALYSIS
-- ------------------------------------------------------------

CREATE OR REPLACE TABLE category_analysis AS

SELECT
    o.order_id,

    poc.product_category,

    r.review_score,

    CASE
        WHEN
            o.order_delivered_customer_date IS NOT NULL
            AND
            o.order_estimated_delivery_date IS NOT NULL
            AND
            CAST(o.order_delivered_customer_date AS TIMESTAMP)
            >
            CAST(o.order_estimated_delivery_date AS TIMESTAMP)
        THEN 1
        ELSE 0
    END AS late_delivery_flag,

    CASE
        WHEN r.review_score <= 2
        THEN 1
        ELSE 0
    END AS poor_experience_flag

FROM orders o

INNER JOIN review_one_per_order r
    ON o.order_id = r.order_id

INNER JOIN primary_order_category poc
    ON o.order_id = poc.order_id

WHERE
    o.order_delivered_customer_date IS NOT NULL

    AND

    o.order_estimated_delivery_date IS NOT NULL;

-- ------------------------------------------------------------
-- VALIDATION
-- ------------------------------------------------------------

SELECT
    COUNT(*) AS analysis_rows,
    COUNT(DISTINCT order_id) AS unique_orders
FROM category_analysis;

-- ------------------------------------------------------------
-- CATEGORY METRICS
-- ------------------------------------------------------------

SELECT

    product_category,

    COUNT(*) AS reviewed_orders,

    ROUND(
        AVG(review_score),
        3
    ) AS average_review_score,

    ROUND(
        AVG(poor_experience_flag) * 100,
        2
    ) AS poor_experience_percentage,

    ROUND(
        AVG(late_delivery_flag) * 100,
        2
    ) AS late_delivery_percentage

FROM category_analysis

GROUP BY product_category

HAVING COUNT(*) >= 100

ORDER BY
    poor_experience_percentage DESC;