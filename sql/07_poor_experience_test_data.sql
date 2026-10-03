-- STEP 7: POOR CUSTOMER EXPERIENCE STATISTICAL TEST
-- Grain: ONE ROW PER REVIEWED ORDER
-- Compare Late vs On-time/Early

CREATE OR REPLACE TABLE orders AS
SELECT *
FROM read_csv_auto('data/raw/olist_orders_dataset.csv');

CREATE OR REPLACE TABLE reviews AS
SELECT *
FROM read_csv_auto('data/raw/olist_order_reviews_dataset.csv');

-- One review score per order
CREATE OR REPLACE TABLE review_one_per_order AS
SELECT
    order_id,
    AVG(review_score) AS review_score
FROM reviews
GROUP BY order_id;

-- Order-level analysis dataset
CREATE OR REPLACE TABLE poor_experience_analysis AS
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
    END AS delivery_group,

    CASE
        WHEN r.review_score <= 2 THEN 1
        ELSE 0
    END AS poor_experience_flag

FROM orders o

INNER JOIN review_one_per_order r
    ON o.order_id = r.order_id

WHERE
    o.order_delivered_customer_date IS NOT NULL
    AND o.order_estimated_delivery_date IS NOT NULL;