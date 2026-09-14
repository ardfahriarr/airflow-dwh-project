CREATE SCHEMA IF NOT EXISTS dwh;

CREATE TABLE IF NOT EXISTS dwh.fact_sales (
    sales_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    transaction_id VARCHAR(50) NOT NULL,
    transaction_item_id VARCHAR(50) NOT NULL,

    customer_key INTEGER,
    product_key INTEGER,
    date_key INTEGER,
    campaign_key INTEGER,

    quantity INTEGER NOT NULL,
    unit_price NUMERIC(18, 2) NOT NULL,
    sales_amount NUMERIC(18, 2) NOT NULL,

    CONSTRAINT uq_fact_sales_transaction_item
        UNIQUE (transaction_id, transaction_item_id),

    CONSTRAINT fk_fact_sales_customer
        FOREIGN KEY (customer_key)
        REFERENCES dwh.dim_customer(customer_key),

    CONSTRAINT fk_fact_sales_product
        FOREIGN KEY (product_key)
        REFERENCES dwh.dim_product(product_key),

    CONSTRAINT fk_fact_sales_date
        FOREIGN KEY (date_key)
        REFERENCES dwh.dim_date(date_key),

    CONSTRAINT fk_fact_sales_campaign
        FOREIGN KEY (campaign_key)
        REFERENCES dwh.dim_campaign(campaign_key)
);

INSERT INTO dwh.fact_sales (
    transaction_id,
    transaction_item_id,
    customer_key,
    product_key,
    date_key,
    campaign_key,
    quantity,
    unit_price,
    sales_amount
)
SELECT
    t.transaction_id,
    ti.transaction_item_id,

    dc.customer_key,
    dp.product_key,

    dd.date_key,

    campaign.campaign_key,

    ti.quantity,
    ti.price AS unit_price,

    ti.quantity * ti.price AS sales_amount

FROM staging.transactions AS t

JOIN staging.transaction_items AS ti
    ON t.transaction_id = ti.transaction_id

LEFT JOIN dwh.dim_customer AS dc
    ON t.customer_id = dc.customer_id

LEFT JOIN dwh.dim_product AS dp
    ON ti.product_id = dp.product_id

LEFT JOIN dwh.dim_date AS dd
    ON DATE(t.transaction_date) = dd.full_date

LEFT JOIN LATERAL (
    SELECT
        dcamp.campaign_key
    FROM dwh.dim_campaign AS dcamp
    WHERE DATE(t.transaction_date)
          BETWEEN dcamp.start_date AND dcamp.end_date
    ORDER BY
        dcamp.start_date DESC,
        dcamp.campaign_id
    LIMIT 1
) AS campaign
    ON TRUE

ON CONFLICT (transaction_id, transaction_item_id)
DO UPDATE SET
    customer_key = EXCLUDED.customer_key,
    product_key = EXCLUDED.product_key,
    date_key = EXCLUDED.date_key,
    campaign_key = EXCLUDED.campaign_key,
    quantity = EXCLUDED.quantity,
    unit_price = EXCLUDED.unit_price,
    sales_amount = EXCLUDED.sales_amount;