CREATE SCHEMA IF NOT EXISTS dwh;

CREATE TABLE IF NOT EXISTS dwh.dim_product (
    product_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    product_name VARCHAR(255),
    category VARCHAR(100),
    price NUMERIC(18, 2),

    CONSTRAINT uq_dim_product_product_id
        UNIQUE (product_id)
);

INSERT INTO dwh.dim_product (
    product_id,
    product_name,
    category,
    price
)
SELECT
    product_id,
    product_name,
    category,
    price
FROM staging.products
ON CONFLICT (product_id)
DO UPDATE SET
    product_name = EXCLUDED.product_name,
    category = EXCLUDED.category,
    price = EXCLUDED.price;