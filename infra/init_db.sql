CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- raw ingestion table (append-only)
CREATE TABLE IF NOT EXISTS raw_sales_events (
  event_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  event_time timestamptz NOT NULL,
  order_id text NOT NULL,
  customer_id text,
  product_id text,
  store_id text,
  quantity integer,
  price numeric(12,2),
  currency text,
  event_type text, -- e.g., 'order', 'refund'
  raw_payload jsonb
);

-- dimension examples
CREATE TABLE IF NOT EXISTS dim_product (
  product_id text PRIMARY KEY,
  product_name text,
  category text,
  brand text
);

CREATE TABLE IF NOT EXISTS dim_customer (
  customer_id text PRIMARY KEY,
  customer_name text,
  customer_tier text
);

CREATE TABLE IF NOT EXISTS dim_store (
  store_id text PRIMARY KEY,
  store_name text,
  region text
);

-- fact table (denormalized for analytics)
CREATE TABLE IF NOT EXISTS fact_sales (
  sale_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  event_time timestamptz NOT NULL,
  order_id text,
  customer_id text,
  product_id text,
  store_id text,
  quantity integer,
  price numeric(12,2),
  revenue numeric(12,2),
  processed_at timestamptz DEFAULT now()
);

-- indexes for query performance on common filters
CREATE INDEX IF NOT EXISTS idx_fact_sales_event_time ON fact_sales (event_time);
CREATE INDEX IF NOT EXISTS idx_fact_sales_product ON fact_sales (product_id);
CREATE INDEX IF NOT EXISTS idx_fact_sales_store ON fact_sales (store_id);
