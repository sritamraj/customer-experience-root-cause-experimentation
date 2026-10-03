-- ============================================================
-- PROJECT #3
-- CUSTOMER EXPERIENCE ROOT-CAUSE & EXPERIMENTATION ANALYTICS
--
-- STEP 2: BUILD ORDER-LEVEL CUSTOMER EXPERIENCE DATASET
-- ============================================================


-- ============================================================
-- 1. LOAD BASE TABLES
-- ============================================================

CREATE OR REPLACE TABLE orders AS
SELECT *
FROM read_csv_auto('data/raw/olist_orders_dataset.csv');

CREATE OR REPLACE TABLE customers AS
SELECT *
FROM read_csv_auto('data/raw/olist_customers_dataset.csv');

CREATE OR REPLACE TABLE reviews AS
SELECT *
FROM read_csv_auto('data/raw/olist_order_reviews_dataset.csv');

CREATE OR REPLACE TABLE order_items AS
SELECT *
FROM read_csv_auto('data/raw/olist_order_items_dataset.csv');

CREATE OR REPLACE TABLE payments AS
SELECT *
FROM read_csv_auto('data/raw/olist_order_payments_dataset.csv');


-- ============================================================
-- 2. AGGREGATE ORDER ITEMS
-- ============================================================

CREATE OR REPLACE TABLE order_item_summary AS

SELECT
    order_id,

    COUNT(*) AS item_count,

    COUNT(DISTINCT product_id) AS unique_product_count,

    COUNT(DISTINCT seller_id) AS unique_seller_count,

    SUM(price) AS merchandise_value,

    SUM(freight_value) AS freight_value,

    SUM(price + freight_value) AS total_item_value

FROM order_items

GROUP BY order_id;


-- ============================================================
-- 3. AGGREGATE PAYMENTS
-- ============================================================

CREATE OR REPLACE TABLE payment_summary AS

SELECT

    order_id,

    SUM(payment_value) AS total_payment_value,

    COUNT(*) AS payment_count,

    MAX(payment_installments) AS max_installments

FROM payments

GROUP BY order_id;


-- ============================================================
-- 4. CUSTOMER-LEVEL ORDER COUNT
-- ============================================================

CREATE OR REPLACE TABLE customer_order_summary AS

SELECT

    customer_id,

    COUNT(*) AS customer_order_count

FROM orders

GROUP BY customer_id;


-- ============================================================
-- 5. BUILD CUSTOMER EXPERIENCE BASE TABLE
-- ============================================================

CREATE OR REPLACE TABLE customer_experience_base AS

SELECT

    o.order_id,

    o.customer_id,

    c.customer_unique_id,

    c.customer_city,

    c.customer_state,

    o.order_status,

    CAST(o.order_purchase_timestamp AS TIMESTAMP)
        AS order_purchase_timestamp,

    CAST(o.order_approved_at AS TIMESTAMP)
        AS order_approved_at,

    CAST(o.order_delivered_carrier_date AS TIMESTAMP)
        AS order_delivered_carrier_date,

    CAST(o.order_delivered_customer_date AS TIMESTAMP)
        AS order_delivered_customer_date,

    CAST(o.order_estimated_delivery_date AS TIMESTAMP)
        AS order_estimated_delivery_date,


    -- ========================================================
    -- DELIVERY METRICS
    -- ========================================================

    CASE

        WHEN o.order_delivered_customer_date IS NOT NULL

        THEN DATE_DIFF(
            'day',
            CAST(o.order_purchase_timestamp AS DATE),
            CAST(o.order_delivered_customer_date AS DATE)
        )

        ELSE NULL

    END AS actual_delivery_days,


    CASE

        WHEN o.order_estimated_delivery_date IS NOT NULL

        THEN DATE_DIFF(
            'day',
            CAST(o.order_purchase_timestamp AS DATE),
            CAST(o.order_estimated_delivery_date AS DATE)
        )

        ELSE NULL

    END AS estimated_delivery_days,


    CASE

        WHEN
            o.order_delivered_customer_date IS NOT NULL
            AND o.order_estimated_delivery_date IS NOT NULL

        THEN DATE_DIFF(
            'day',
            CAST(o.order_estimated_delivery_date AS DATE),
            CAST(o.order_delivered_customer_date AS DATE)
        )

        ELSE NULL

    END AS delivery_delay_days,


    CASE

        WHEN
            o.order_delivered_customer_date IS NOT NULL
            AND o.order_estimated_delivery_date IS NOT NULL
            AND o.order_delivered_customer_date
                > o.order_estimated_delivery_date

        THEN 1

        WHEN
            o.order_delivered_customer_date IS NOT NULL
            AND o.order_estimated_delivery_date IS NOT NULL

        THEN 0

        ELSE NULL

    END AS late_delivery_flag,


    -- ========================================================
    -- REVIEW / CUSTOMER EXPERIENCE
    -- ========================================================

    r.review_score,

    CASE

        WHEN r.review_score <= 2 THEN 1

        WHEN r.review_score >= 4 THEN 0

        ELSE NULL

    END AS poor_experience_flag,


    -- ========================================================
    -- ORDER ECONOMICS
    -- ========================================================

    oi.item_count,

    oi.unique_product_count,

    oi.unique_seller_count,

    oi.merchandise_value,

    oi.freight_value,

    oi.total_item_value,

    p.total_payment_value,

    p.payment_count,

    p.max_installments,


    -- ========================================================
    -- CUSTOMER HISTORY
    -- ========================================================

    cos.customer_order_count

FROM orders o

LEFT JOIN customers c
    ON o.customer_id = c.customer_id

LEFT JOIN reviews r
    ON o.order_id = r.order_id

LEFT JOIN order_item_summary oi
    ON o.order_id = oi.order_id

LEFT JOIN payment_summary p
    ON o.order_id = p.order_id

LEFT JOIN customer_order_summary cos
    ON o.customer_id = cos.customer_id;


-- ============================================================
-- 6. BASIC VALIDATION
-- ============================================================

SELECT

    COUNT(*) AS total_orders,

    COUNT(DISTINCT order_id) AS unique_orders,

    COUNT(review_score) AS orders_with_reviews,

    COUNT(late_delivery_flag) AS orders_with_delivery_status,

    COUNT(poor_experience_flag) AS orders_with_poor_experience_label

FROM customer_experience_base;


-- ============================================================
-- 7. ORDER STATUS DISTRIBUTION
-- ============================================================

SELECT

    order_status,

    COUNT(*) AS orders,

    ROUND(
        100.0 * COUNT(*) /
        SUM(COUNT(*)) OVER (),
        2
    ) AS percentage

FROM customer_experience_base

GROUP BY order_status

ORDER BY orders DESC;


-- ============================================================
-- 8. CUSTOMER EXPERIENCE SUMMARY
-- ============================================================

SELECT

    ROUND(AVG(review_score), 3)
        AS average_review_score,

    ROUND(
        100.0 * AVG(poor_experience_flag),
        2
    )
        AS poor_experience_percentage,

    ROUND(
        100.0 * AVG(late_delivery_flag),
        2
    )
        AS late_delivery_percentage,

    ROUND(
        AVG(delivery_delay_days),
        2
    )
        AS average_delivery_delay_days,

    ROUND(
        AVG(total_payment_value),
        2
    )
        AS average_order_value

FROM customer_experience_base;