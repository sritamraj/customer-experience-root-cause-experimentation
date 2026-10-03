-- ============================================================
-- PROJECT #3
-- STEP 3: DELIVERY PERFORMANCE VS CUSTOMER EXPERIENCE
-- ============================================================

CREATE OR REPLACE TABLE orders AS
SELECT *
FROM read_csv_auto('data/raw/olist_orders_dataset.csv');

CREATE OR REPLACE TABLE reviews AS
SELECT *
FROM read_csv_auto('data/raw/olist_order_reviews_dataset.csv');


-- ============================================================
-- DELIVERY + REVIEW DATASET
-- ============================================================

CREATE OR REPLACE TABLE delivery_cx AS

SELECT

    o.order_id,
    o.order_status,

    CAST(o.order_purchase_timestamp AS TIMESTAMP)
        AS order_purchase_timestamp,

    CAST(o.order_delivered_customer_date AS TIMESTAMP)
        AS delivered_date,

    CAST(o.order_estimated_delivery_date AS TIMESTAMP)
        AS estimated_date,

    r.review_score,

    CASE

        WHEN
            o.order_delivered_customer_date IS NOT NULL
            AND o.order_estimated_delivery_date IS NOT NULL
            AND o.order_delivered_customer_date
                > o.order_estimated_delivery_date

        THEN 'Late'

        WHEN
            o.order_delivered_customer_date IS NOT NULL
            AND o.order_estimated_delivery_date IS NOT NULL

        THEN 'On-time / Early'

        ELSE 'Unknown'

    END AS delivery_group,

    CASE

        WHEN r.review_score <= 2
        THEN 1

        WHEN r.review_score >= 4
        THEN 0

        ELSE NULL

    END AS poor_experience_flag

FROM orders o

LEFT JOIN reviews r
    ON o.order_id = r.order_id;


-- ============================================================
-- 1. DELIVERY GROUP DISTRIBUTION
-- ============================================================

SELECT

    delivery_group,

    COUNT(*) AS orders,

    ROUND(
        100.0 * COUNT(*) /
        SUM(COUNT(*)) OVER (),
        2
    ) AS percentage

FROM delivery_cx

GROUP BY delivery_group

ORDER BY orders DESC;


-- ============================================================
-- 2. CUSTOMER EXPERIENCE BY DELIVERY GROUP
-- ============================================================

SELECT

    delivery_group,

    COUNT(review_score) AS reviewed_orders,

    ROUND(
        AVG(review_score),
        3
    ) AS average_review_score,

    ROUND(
        100.0 * AVG(poor_experience_flag),
        2
    ) AS poor_experience_percentage

FROM delivery_cx

WHERE review_score IS NOT NULL

GROUP BY delivery_group

ORDER BY average_review_score;


-- ============================================================
-- 3. REVIEW SCORE DISTRIBUTION
-- ============================================================

SELECT

    delivery_group,

    review_score,

    COUNT(*) AS orders

FROM delivery_cx

WHERE review_score IS NOT NULL

GROUP BY
    delivery_group,
    review_score

ORDER BY
    delivery_group,
    review_score;


-- ============================================================
-- 4. DELIVERY DELAY BUCKETS
-- ============================================================

SELECT

    CASE

        WHEN
            delivered_date IS NULL
            OR estimated_date IS NULL
        THEN 'Unknown'

        WHEN delivered_date <= estimated_date
        THEN 'Early / On-time'

        WHEN DATE_DIFF(
            'day',
            CAST(estimated_date AS DATE),
            CAST(delivered_date AS DATE)
        ) BETWEEN 1 AND 3
        THEN '1-3 days late'

        WHEN DATE_DIFF(
            'day',
            CAST(estimated_date AS DATE),
            CAST(delivered_date AS DATE)
        ) BETWEEN 4 AND 7
        THEN '4-7 days late'

        WHEN DATE_DIFF(
            'day',
            CAST(estimated_date AS DATE),
            CAST(delivered_date AS DATE)
        ) BETWEEN 8 AND 14
        THEN '8-14 days late'

        ELSE '15+ days late'

    END AS delay_bucket,

    COUNT(*) AS orders,

    ROUND(
        AVG(review_score),
        3
    ) AS average_review_score,

    ROUND(
        100.0 * AVG(poor_experience_flag),
        2
    ) AS poor_experience_percentage

FROM delivery_cx

WHERE review_score IS NOT NULL

GROUP BY delay_bucket

ORDER BY
    CASE delay_bucket
        WHEN 'Early / On-time' THEN 1
        WHEN '1-3 days late' THEN 2
        WHEN '4-7 days late' THEN 3
        WHEN '8-14 days late' THEN 4
        WHEN '15+ days late' THEN 5
        ELSE 6
    END;