CREATE SCHEMA IF NOT EXISTS dwh;

CREATE TABLE IF NOT EXISTS dwh.dim_campaign (
    campaign_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    campaign_id VARCHAR(50) NOT NULL,
    campaign_name VARCHAR(255),
    start_date DATE,
    end_date DATE,
    channel VARCHAR(100),

    CONSTRAINT uq_dim_campaign_campaign_id
        UNIQUE (campaign_id),

    CONSTRAINT chk_dim_campaign_date
        CHECK (end_date >= start_date)
);

INSERT INTO dwh.dim_campaign (
    campaign_id,
    campaign_name,
    start_date,
    end_date,
    channel
)
SELECT
    campaign_id,
    campaign_name,
    start_date,
    end_date,
    channel
FROM staging.marketing_campaigns
ON CONFLICT (campaign_id)
DO UPDATE SET
    campaign_name = EXCLUDED.campaign_name,
    start_date = EXCLUDED.start_date,
    end_date = EXCLUDED.end_date,
    channel = EXCLUDED.channel;