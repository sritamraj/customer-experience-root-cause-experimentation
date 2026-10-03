-- ============================================================
-- PROJECT #3 — SELLER × DELIVERY CONTROL ANALYSIS
-- ============================================================

DROP VIEW IF EXISTS seller_delivery_summary;

CREATE VIEW seller_delivery_summary AS

WITH

orders AS (
    SELECT
        order_id,
        order_status,
        order_delivered_customer_date,
        order_estimated_delivery_date,
        order_purchase_timestamp
    FROM read_csv_auto(
        'data/raw/olist_orders_dataset.csv'
    )
),

reviews_raw AS (
    SELECT
        order_id,
        review_score
    FROM read_csv_auto(
        'data/raw/olist_order_reviews_dataset.csv'
    )
),

review_one_per_order AS (
    SELECT
        order_id,
        AVG(review_score) AS review_score
    FROM reviews_raw
    GROUP BY order_id
),

order_items AS (
    SELECT
        order_id,
        seller_id,
        price,
        freight_value
    FROM read_csv_auto(
        'data/raw/olist_order_items_dataset.csv'
    )
),

order_seller_value AS (
    SELECT
        order_id,
        seller_id,
        SUM(
            COALESCE(price, 0)
            + COALESCE(freight_value, 0)
        ) AS seller_order_value
    FROM order_items
    GROUP BY
        order_id,
        seller_id
),

primary_order_seller AS (
    SELECT
        order_id,
        seller_id
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
            ) AS rn

        FROM order_seller_value
    )
    WHERE rn = 1
),

base AS (
    SELECT
        o.order_id,
        p.seller_id,
        r.review_score,

        CASE

            WHEN
                o.order_delivered_customer_date IS NOT NULL
                AND o.order_estimated_delivery_date IS NOT NULL
                AND o.order_delivered_customer_date
                    <= o.order_estimated_delivery_date

            THEN 'On-time/Early'

            WHEN
                o.order_delivered_customer_date IS NOT NULL
                AND o.order_estimated_delivery_date IS NOT NULL
                AND o.order_delivered_customer_date
                    > o.order_estimated_delivery_date

            THEN 'Late'

            ELSE 'Unknown'

        END AS delivery_group,

        CASE
            WHEN r.review_score <= 2
            THEN 1
            ELSE 0
        END AS poor_experience

    FROM orders o

    INNER JOIN review_one_per_order r
        ON o.order_id = r.order_id

    INNER JOIN primary_order_seller p
        ON o.order_id = p.order_id

    WHERE
        o.order_delivered_customer_date IS NOT NULL
        AND o.order_estimated_delivery_date IS NOT NULL
),

seller_delivery_summary AS (

    SELECT

        seller_id,

        delivery_group,

        COUNT(*) AS orders,

        AVG(review_score)
            AS average_review_score,

        AVG(poor_experience) * 100
            AS poor_experience_percentage

    FROM base

    WHERE delivery_group IN (
        'Late',
        'On-time/Early'
    )

    GROUP BY
        seller_id,
        delivery_group

    HAVING COUNT(*) >= 30
)

SELECT *
FROM seller_delivery_summary;