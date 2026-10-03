-- STEP 6: STATISTICAL TEST DATA
-- Grain: ONE ROW PER REVIEWED ORDER
-- Purpose: Prepare Late vs On-time/Early samples for Welch's t-test

CREATE OR REPLACE TABLE orders AS
SELECT *
FROM read_csv_auto('data/raw/olist_orders_dataset.csv');

CREATE OR REPLACE TABLE reviews AS
SELECT *
FROM read_csv_auto('data/raw/olist_order_reviews_dataset.csv');

-- Aggregate reviews to ONE ROW PER ORDER
CREATE OR REPLACE TABLE review_one_per_order AS
SELECT
    order_id,
    AVG(review_score) AS review_score
FROM reviews
GROUP BY order_id;

-- Create analysis dataset
CREATE OR REPLACE TABLE delivery_review_analysis AS
SELECT
    o.order_id,
    r.review_score,

    CASE
        WHEN o.order_delivered_customer_date IS NOT NULL
         AND o.order_estimated_delivery_date IS NOT NULL
         AND CAST(o.order_delivered_customer_date AS TIMESTAMP)
             > CAST(o.order_estimated_delivery_date AS TIMESTAMP)
        THEN 'Late'

        WHEN o.order_delivered_customer_date IS NOT NULL
         AND o.order_estimated_delivery_date IS NOT NULL
        THEN 'On-time / Early'

        ELSE 'Unknown'
    END AS delivery_group

FROM orders o
INNER JOIN review_one_per_order r
    ON o.order_id = r.order_id

WHERE
    o.order_delivered_customer_date IS NOT NULL
    AND o.order_estimated_delivery_date IS NOT NULL;