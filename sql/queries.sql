-- Restaurant Analytics SQL Queries
-- Table: restaurants_clean (imported from data/cleaned/restaurants_clean.csv)
-- Load in SQLite:
--   .open restaurant.db
--   .mode csv
--   .import --skip 1 data/cleaned/restaurants_clean.csv restaurants_clean

-- 1. Overall summary
SELECT
    COUNT(*) AS total_restaurants,
    ROUND(AVG(stars), 2) AS avg_rating,
    SUM(is_open) AS currently_open,
    ROUND(SUM(is_open) * 100.0 / COUNT(*), 1) AS pct_open
FROM restaurants_clean;

-- 2. Rating distribution
SELECT
    stars,
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS pct
FROM restaurants_clean
GROUP BY stars
ORDER BY stars;

-- 3. Top 15 cities by restaurant count and avg rating
SELECT
    city,
    COUNT(*) AS restaurants,
    ROUND(AVG(stars), 2) AS avg_rating,
    SUM(review_count) AS total_reviews
FROM restaurants_clean
GROUP BY city
ORDER BY restaurants DESC
LIMIT 15;

-- 4. Rating tier breakdown
SELECT
    rating_tier,
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS pct,
    ROUND(AVG(review_count), 0) AS avg_reviews
FROM restaurants_clean
WHERE rating_tier IS NOT NULL
GROUP BY rating_tier
ORDER BY CASE rating_tier WHEN 'top' THEN 1 WHEN 'high' THEN 2 WHEN 'medium' THEN 3 ELSE 4 END;

-- 5. Open vs closed: rating comparison
SELECT
    CASE is_open WHEN 1 THEN 'Open' ELSE 'Closed' END AS status,
    COUNT(*) AS count,
    ROUND(AVG(stars), 2) AS avg_rating,
    ROUND(AVG(review_count), 0) AS avg_reviews
FROM restaurants_clean
GROUP BY is_open;

-- 6. Price range impact on rating
SELECT
    pricerange2 AS price_range,
    COUNT(*) AS count,
    ROUND(AVG(stars), 2) AS avg_rating,
    ROUND(AVG(review_count), 0) AS avg_reviews
FROM restaurants_clean
WHERE pricerange2 IS NOT NULL
GROUP BY pricerange2
ORDER BY pricerange2;

-- 7. Delivery vs no delivery
SELECT
    CASE delivery WHEN '1' THEN 'Has Delivery' ELSE 'No Delivery' END AS delivery_status,
    COUNT(*) AS count,
    ROUND(AVG(stars), 2) AS avg_rating,
    ROUND(AVG(review_count), 0) AS avg_reviews
FROM restaurants_clean
WHERE delivery IS NOT NULL
GROUP BY delivery;

-- 8. Reservations impact on rating
SELECT
    CASE reservations WHEN '1' THEN 'Takes Reservations' ELSE 'No Reservations' END AS res_status,
    COUNT(*) AS count,
    ROUND(AVG(stars), 2) AS avg_rating
FROM restaurants_clean
WHERE reservations IS NOT NULL
GROUP BY reservations;

-- 9. Operational matrix: price range x delivery
SELECT
    pricerange2 AS price_range,
    CASE delivery WHEN '1' THEN 'Yes' ELSE 'No' END AS delivery,
    COUNT(*) AS count,
    ROUND(AVG(stars), 2) AS avg_rating
FROM restaurants_clean
WHERE pricerange2 IS NOT NULL AND delivery IS NOT NULL
GROUP BY pricerange2, delivery
ORDER BY pricerange2, delivery;

-- 10. Cities with highest avg rating (min 100 restaurants)
SELECT
    city,
    COUNT(*) AS restaurants,
    ROUND(AVG(stars), 2) AS avg_rating,
    ROUND(AVG(review_count), 0) AS avg_reviews
FROM restaurants_clean
GROUP BY city
HAVING COUNT(*) >= 100
ORDER BY avg_rating DESC
LIMIT 10;

-- 11. Cities with lowest survival rate
SELECT
    city,
    COUNT(*) AS total,
    SUM(is_open) AS open_count,
    ROUND(SUM(is_open) * 100.0 / COUNT(*), 1) AS pct_open
FROM restaurants_clean
GROUP BY city
HAVING COUNT(*) >= 100
ORDER BY pct_open ASC
LIMIT 10;

-- 12. Operational profile of high-rated restaurants (>=4.0 stars)
SELECT
    ROUND(AVG(CASE WHEN delivery = '1' THEN 1.0 ELSE 0.0 END) * 100, 1) AS pct_delivery,
    ROUND(AVG(CASE WHEN takeout = '1' THEN 1.0 ELSE 0.0 END) * 100, 1) AS pct_takeout,
    ROUND(AVG(CASE WHEN reservations = '1' THEN 1.0 ELSE 0.0 END) * 100, 1) AS pct_reservations,
    ROUND(AVG(CASE WHEN outdoorseating = '1' THEN 1.0 ELSE 0.0 END) * 100, 1) AS pct_outdoor,
    ROUND(AVG(review_count), 0) AS avg_reviews,
    ROUND(AVG(CAST(pricerange2 AS REAL)), 2) AS avg_price_range
FROM restaurants_clean
WHERE stars >= 4.0;
