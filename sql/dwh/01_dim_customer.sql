CREATE SCHEMA IF NOT EXISTS dwh;

CREATE TABLE IF NOT EXISTS dwh.dim_customer (
    customer_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    name VARCHAR(255),
    email VARCHAR(255),
    city VARCHAR(100),
    signup_date DATE,

    CONSTRAINT uq_dim_customer_customer_id
        UNIQUE (customer_id)
);

INSERT INTO dwh.dim_customer (
    customer_id,
    name,
    email,
    city,
    signup_date
)
SELECT
    customer_id,
    name,
    email,
    city,
    signup_date
FROM staging.customers
ON CONFLICT (customer_id)
DO UPDATE SET
    name = EXCLUDED.name,
    email = EXCLUDED.email,
    city = EXCLUDED.city,
    signup_date = EXCLUDED.signup_date;