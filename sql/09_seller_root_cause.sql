-- STEP 8B-FIX
-- SELLER ROOT-CAUSE ANALYSIS
-- Grain: ONE ROW PER ORDER
--
-- Representative seller:
-- Seller contributing the highest item value within the order.

CREATE OR REPLACE TABLE orders AS
SELECT *
FROM read_csv_auto('data/raw/olist_orders_dataset.csv');

CREATE OR REPLACE TABLE reviews AS
SELECT *
FROM read_csv_auto('data/raw/olist_order_reviews_dataset.csv');

CREATE OR REPLACE TABLE order_items AS
SELECT *
FROM read_csv_auto('data/raw/olist_order_items_dataset.csv');

CREATE OR REPLACE TABLE sellers AS
SELECT *
FROM read_csv_auto('data/raw/olist_sellers_dataset.csv');

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
-- SELLER VALUE WITHIN EACH ORDER
-- ------------------------------------------------------------

CREATE OR REPLACE TABLE order_seller_value AS
SELECT

    oi.order_id,

    oi.seller_id,

    SUM(
        COALESCE(oi.price, 0)
        + COALESCE(oi.freight_value, 0)
    ) AS seller_order_value

FROM order_items oi

GROUP BY
    oi.order_id,
    oi.seller_id;

-- ------------------------------------------------------------
-- SELECT ONE REPRESENTATIVE SELLER PER ORDER
-- Highest-value seller wins.
-- Seller ID is used as deterministic tie-breaker.
-- ------------------------------------------------------------

CREATE OR REPLACE TABLE primary_order_seller AS

SELECT

    order_id,

    seller_id,

    seller_order_value

FROM (

    SELECT

        order_id,

        seller_id,

        seller_order_value,

        ROW_NUMBER() OVER (

            PARTITION BY order_id

            ORDER BY
                seller_order_value DESC,
                seller_id

        ) AS seller_rank

    FROM order_seller_value
)

WHERE seller_rank = 1;

-- ------------------------------------------------------------
-- FINAL ORDER-LEVEL SELLER ANALYSIS
-- ------------------------------------------------------------

CREATE OR REPLACE TABLE seller_analysis AS

SELECT

    o.order_id,

    pos.seller_id,

    pos.seller_order_value AS order_value,

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

INNER JOIN primary_order_seller pos
    ON o.order_id = pos.order_id

WHERE

    o.order_delivered_customer_date IS NOT NULL

    AND

    o.order_estimated_delivery_date IS NOT NULL;

-- ------------------------------------------------------------
-- VALIDATE ANALYTICAL GRAIN
-- ------------------------------------------------------------

SELECT

    COUNT(*) AS analysis_rows,

    COUNT(DISTINCT order_id) AS unique_orders

FROM seller_analysis;

-- ------------------------------------------------------------
-- SELLER METRICS
-- Minimum 100 reviewed orders
-- ------------------------------------------------------------

SELECT

    seller_id,

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
    ) AS late_delivery_percentage,

    ROUND(
        AVG(order_value),
        2
    ) AS average_order_value

FROM seller_analysis

GROUP BY seller_id

HAVING COUNT(*) >= 100

ORDER BY
    poor_experience_percentage DESC;