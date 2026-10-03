-- ============================================================
-- PROJECT #3
-- STEP 12 — EXPERIMENT DESIGN DATASET
-- ============================================================

WITH orders AS (
    SELECT *
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

base AS (
    SELECT
        o.order_id,

        CAST(
            o.order_delivered_customer_date
            AS DATE
        ) AS delivered_date,

        CAST(
            o.order_estimated_delivery_date
            AS DATE
        ) AS estimated_date,

        r.review_score

    FROM orders o

    INNER JOIN reviews r
        ON o.order_id = r.order_id

    WHERE
        o.order_delivered_customer_date IS NOT NULL
        AND o.order_estimated_delivery_date IS NOT NULL
),

experiment_population AS (

    SELECT
        order_id,
        review_score,

        CASE
            WHEN delivered_date > estimated_date
            THEN 1
            ELSE 0
        END AS late_delivery,

        CASE
            WHEN review_score <= 2
            THEN 1
            ELSE 0
        END AS poor_experience

    FROM base
)

SELECT
    COUNT(*) AS experiment_population,

    SUM(late_delivery) AS late_orders,

    SUM(poor_experience) AS poor_experience_orders,

    AVG(late_delivery) AS late_delivery_rate,

    AVG(poor_experience) AS poor_experience_rate

FROM experiment_population;