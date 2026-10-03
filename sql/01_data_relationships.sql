-- PROJECT #3
-- Customer Experience Root-Cause & Experimentation Analytics
-- Step 1: Understand table relationships

-- ============================================================
-- PRIMARY KEYS / IDENTIFIERS
-- ============================================================

-- customers
-- customer_id
-- customer_unique_id

-- orders
-- order_id
-- customer_id

-- order_reviews
-- review_id
-- order_id

-- order_items
-- order_id
-- order_item_id
-- product_id
-- seller_id

-- payments
-- order_id
-- payment_sequential

-- products
-- product_id

-- sellers
-- seller_id


-- ============================================================
-- CORE RELATIONSHIP
-- ============================================================

-- customers
--      |
--      | customer_id
--      v
-- orders
--      |
--      | order_id
--      +----------------------+
--      |                      |
--      v                      v
-- order_reviews          order_items
--                             |
--                     +-------+-------+
--                     |               |
--                     v               v
--                  products        sellers
--
-- orders
--   |
--   +---- payments


-- ============================================================
-- PROJECT #3 BUSINESS FLOW
-- ============================================================

-- Customer
--     ↓
-- Order
--     ↓
-- Delivery Performance
--     ↓
-- Review Score
--     ↓
-- Product / Seller / Payment
--     ↓
-- Root Cause Analysis
--     ↓
-- Statistical Testing
--     ↓
-- Experiment Design
--     ↓
-- Business Recommendation