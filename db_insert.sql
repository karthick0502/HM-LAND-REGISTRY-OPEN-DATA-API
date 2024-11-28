-- Prepopulating Property Types
INSERT INTO property_types (property_type_code, property_type_description)
VALUES 
    ('D', 'Detached'),
    ('S', 'Semi-Detached'),
    ('T', 'Terraced'),
    ('F', 'Flats/Maisonettes'),
    ('O', 'Other');

-- Prepopulating Tenures
INSERT INTO tenures (tenure_code, tenure_description)
VALUES 
    ('F', 'Freehold'),
    ('L', 'Leasehold');

-- Prepopulating PPD Categories
INSERT INTO ppd_categories (ppd_category_code, ppd_category_description)
VALUES 
    ('A', 'Standard Price Paid entry, includes single residential property sold for value'),
    ('B', 'Additional Price Paid entry including repossessions, buy-to-lets, transfers to non-private individuals');

-- Prepopulating Record Statuses
INSERT INTO record_statuses (record_status_code, record_status_description)
VALUES 
    ('A', 'Addition'),
    ('C', 'Change'),
    ('D', 'Delete');

-- Insert the first record into property_transactions
INSERT INTO property_transactions (
    transaction_unique_id,
    price,
    date_of_transfer,
    postcode,
    property_type_id,
    old_new,
    tenure_id,
    paon,
    saon,
    street,
    locality,
    town_city,
    district,
    county,
    ppd_category_id,
    record_status_id,
    avg_price_by_property_type,
    address
)
VALUES (
    '237B17FD-8F57-22AC-E063-4804A8C0EA3A', -- transaction_unique_id
    415000, -- price
    '2021-02-02', -- date_of_transfer
    'EN9 2BQ', -- postcode
    (SELECT property_type_id FROM property_types WHERE property_type_code = 'T'), -- property_type_id for "Terraced"
    'N', -- old_new
    (SELECT tenure_id FROM tenures WHERE tenure_code = 'F'), -- tenure_id for "Freehold"
    'CLAYTON COURT', -- paon
    NULL, -- saon (using NULL if empty)
    'NAZEING ROAD', -- street
    'NAZEING', -- locality
    'WALTHAM ABBEY', -- town_city
    'EPPING FOREST', -- district
    'ESSEX', -- county
    (SELECT ppd_category_id FROM ppd_categories WHERE ppd_category_code = 'A'), -- ppd_category_id for "Standard Price Paid entry"
    (SELECT record_status_id FROM record_statuses WHERE record_status_code = 'A'), -- record_status_id for "Addition"
    0.00, -- avg_price_by_property_type (default)
    CONCAT(
        'CLAYTON COURT', ', ', '6', ', ', 'NAZEING ROAD', ', ', 
        'NAZEING', ', ', 'WALTHAM ABBEY', ', ', 'EPPING FOREST', ', ', 'ESSEX'
    ) -- address (constructed)
);

-- Insert the second record into property_transactions
INSERT INTO property_transactions (
    transaction_unique_id,
    price,
    date_of_transfer,
    postcode,
    property_type_id,
    old_new,
    tenure_id,
    paon,
    saon,
    street,
    locality,
    town_city,
    district,
    county,
    ppd_category_id,
    record_status_id,
    avg_price_by_property_type,
    address
)
VALUES (
    '237B17FD-8F60-22AC-E063-4804A8C0EA3A', -- transaction_unique_id
    525000, -- price
    '2021-06-22', -- date_of_transfer
    'CM9 6ZH', -- postcode
    (SELECT property_type_id FROM property_types WHERE property_type_code = 'D'), -- property_type_id for "Detached"
    'Y', -- old_new
    (SELECT tenure_id FROM tenures WHERE tenure_code = 'F'), -- tenure_id (Duration) for "Freehold"
    '5', -- paon
    NULL, -- saon (using NULL if empty)
    'ANSON CLOSE', -- street
    NULL, -- locality (using NULL if empty)
    'MALDON', -- town_city
    'MALDON', -- district
    'ESSEX', -- county
    (SELECT ppd_category_id FROM ppd_categories WHERE ppd_category_code = 'A'), -- ppd_category_id for "Standard Price Paid entry"
    (SELECT record_status_id FROM record_statuses WHERE record_status_code = 'A'), -- record_status_id for "Addition"
    0.00, -- avg_price_by_property_type (default)
    CONCAT(
        '5', ', ', 'ANSON CLOSE', ', ', 
        'MALDON', ', ', 'MALDON', ', ', 'ESSEX'
    ) -- address (constructed)
);