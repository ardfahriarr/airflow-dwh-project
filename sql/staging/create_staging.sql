CREATE SCHEMA IF NOT EXISTS staging;

CREATE TABLE IF NOT EXISTS staging.customers (
    customer_id VARCHAR(255),
    name VARCHAR(255),
    email VARCHAR(255),
    city VARCHAR(100),
    signup_date DATE
);

CREATE TABLE IF NOT EXISTS staging.products (
    product_id VARCHAR(255),
    product_name VARCHAR(255),
    category VARCHAR(100),
    price NUMERIC(12,2)
);

CREATE TABLE IF NOT EXISTS staging.transactions (
    transaction_id VARCHAR(255),
    customer_id VARCHAR(255),
    transaction_date DATE,
    total_amount NUMERIC(12,2)
);

CREATE TABLE IF NOT EXISTS staging.transaction_items (
    transaction_item_id VARCHAR(255),
    transaction_id VARCHAR(255),
    product_id VARCHAR(255),
    quantity INTEGER,
    price NUMERIC(12,2)
);

CREATE TABLE IF NOT EXISTS staging.marketing_campaigns (
    campaign_id VARCHAR(255),
    campaign_name VARCHAR(255),
    start_date DATE,
    end_date DATE,
    channel VARCHAR(100)
);