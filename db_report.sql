-- Delete the sample record
-- DELETE FROM property_transactions;

-- Average Price and Transaction Count by Property Type and County

SELECT pt.county AS county, ptp.property_type_code AS property_type,
COUNT(pt.transaction_id) AS transaction_count,
AVG(pt.price) AS avg_price
FROM property_transactions pt
JOIN property_types ptp 
ON pt.property_type_id = ptp.property_type_id
GROUP BY pt.county, ptp.property_type_code
ORDER BY transaction_count DESC;

-- High-Value Transactions- Property Price Trends (Above 1 Million)

SELECT transaction_unique_id, price, date_of_transfer,town_city, county, postcode
FROM property_transactions
WHERE price > 1000000
ORDER BY price DESC;


