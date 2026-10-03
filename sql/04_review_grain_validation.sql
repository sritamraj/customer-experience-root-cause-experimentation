-- ============================================================
-- PROJECT #3
-- STEP 4: REVIEW GRAIN VALIDATION
-- ============================================================

CREATE OR REPLACE TABLE reviews AS
SELECT *
FROM read_csv_auto('data/raw/olist_order_reviews_dataset.csv');


-- ============================================================
-- 1. CHECK WHETHER ORDER_ID IS UNIQUE
-- ============================================================

SELECT
    COUNT(*) AS review_rows,
    COUNT(DISTINCT order_id) AS unique_order_ids,
    COUNT(*) - COUNT(DISTINCT order_id) AS duplicate_order_review_rows
FROM reviews;


-- ============================================================
-- 2. FIND ORDERS WITH MULTIPLE REVIEWS
-- ============================================================

SELECT
    order_id,
    COUNT(*) AS review_count
FROM reviews
GROUP BY order_id
HAVING COUNT(*) > 1
ORDER BY review_count DESC
LIMIT 20;


-- ============================================================
-- 3. CREATE ONE REVIEW RECORD PER ORDER
-- ============================================================

CREATE OR REPLACE TABLE review_one_per_order AS

SELECT

    order_id,

    -- Average score if an order has multiple review records
    AVG(review_score) AS review_score,

    COUNT(*) AS review_record_count

FROM reviews

GROUP BY order_id;


-- ============================================================
-- 4. VALIDATE THE NEW GRAIN
-- ============================================================

SELECT

    COUNT(*) AS review_orders,

    COUNT(DISTINCT order_id) AS unique_order_ids

FROM review_one_per_order;