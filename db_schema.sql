-- Table 1: Property Types
CREATE TABLE property_types (
    property_type_id SERIAL PRIMARY KEY,
    property_type_code CHAR(1) NOT NULL UNIQUE,
    property_type_description VARCHAR(50) NOT NULL
);

-- Table 2: (Duration) Tenure 
CREATE TABLE tenures (
    tenure_id SERIAL PRIMARY KEY,
    tenure_code CHAR(1) NOT NULL UNIQUE,
    tenure_description VARCHAR(50) NOT NULL
);

-- Table 3: PPD Categories
CREATE TABLE ppd_categories (
    ppd_category_id SERIAL PRIMARY KEY,
    ppd_category_code CHAR(1) NOT NULL UNIQUE,
    ppd_category_description VARCHAR(255) NOT NULL
);

-- Table 4: Record Statuses
CREATE TABLE record_statuses (
    record_status_id SERIAL PRIMARY KEY,
    record_status_code CHAR(1) NOT NULL UNIQUE,
    record_status_description VARCHAR(255) NOT NULL
);

-- Main Table: Property Transactions
CREATE TABLE property_transactions (
    transaction_id SERIAL PRIMARY KEY,
    transaction_unique_id VARCHAR(100) UNIQUE NOT NULL,
    price NUMERIC(15, 2) NOT NULL,
    date_of_transfer DATE NOT NULL,
    postcode VARCHAR(10) NOT NULL,
    property_type_id INT NOT NULL,
    old_new CHAR(1),
    tenure_id INT NOT NULL,
    paon VARCHAR(255),
    saon VARCHAR(255),
    street VARCHAR(255),
    locality VARCHAR(255),
    town_city VARCHAR(255),
    district VARCHAR(255),
    county VARCHAR(255),
    ppd_category_id INT NOT NULL,
    record_status_id INT NOT NULL,
    avg_price_by_property_type NUMERIC(15, 2),
    address TEXT,
    FOREIGN KEY (property_type_id) REFERENCES property_types (property_type_id),
    FOREIGN KEY (tenure_id) REFERENCES tenures (tenure_id),
    FOREIGN KEY (ppd_category_id) REFERENCES ppd_categories (ppd_category_id),
    FOREIGN KEY (record_status_id) REFERENCES record_statuses (record_status_id)
);

