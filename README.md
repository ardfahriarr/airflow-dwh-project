# Airflow DWH Project

## 1. Gambaran Umum

### Tujuan

Project ini merupakan implementasi Data Engineering Technical Test yang berfokus pada pembangunan pipeline ETL menggunakan Python dan Apache Airflow, serta perancangan Data Warehouse berdasarkan data transaksi dan data master.

Tujuan utama project ini adalah:

- Membuat dan memproses data source/staging menggunakan PostgreSQL.
- Membangun pipeline ETL yang terorkestrasi menggunakan Apache Airflow.
- Merancang Data Warehouse dengan pendekatan star schema.
- Mengolah data transaksi dan transaction items menjadi `fact_sales`.
- Membentuk dimension table untuk customer, product, date, dan campaign.
- Menyediakan dokumentasi mengenai arsitektur, data model, asumsi, serta cara menjalankan pipeline.

### Ruang Lingkup

Pipeline mencakup lima sumber data utama:

- `customers`
- `products`
- `transactions`
- `transaction_items`
- `marketing_campaigns`

Data dari staging kemudian diproses menjadi lima tabel pada layer Data Warehouse:

- `dim_customer`
- `dim_product`
- `dim_date`
- `dim_campaign`
- `fact_sales`

`fact_sales` dibentuk dari kombinasi data `transactions` dan `transaction_items`, sedangkan dimension table digunakan untuk memberikan konteks analitik terhadap data penjualan.

### Teknologi

Teknologi utama yang digunakan dalam project ini:

| Komponen | Teknologi |
|---|---|
| Programming | Python |
| Orchestration | Apache Airflow |
| Database / Staging | PostgreSQL |
| Data Warehouse | PostgreSQL |
| Transformation | SQL |
| Containerization | Docker / Docker Compose |
| Version Control | Git / GitHub |
| Diagram | draw.io |

## 2. Arsitektur Project

### Gambaran Arsitektur

Pipeline ETL pada project ini menggunakan PostgreSQL sebagai source/staging database sekaligus target Data Warehouse, dengan Apache Airflow sebagai orchestration layer.

end-to-end pipeline:

```text
Source Data
      >> Ingestion/Validation Pipeline
          >> PostgreSQL Staging
              >> Data Modelling Process
                  >> Data Warehouse
                      >> PostgreSQL DWH
```
data flow:
```text
staging.customers ---------------------------------->> dim_customer

staging.products ----------------------------------->> dim_product

calendar / date generation ------------------------->> dim_date

staging.marketing_campaigns ------------------------>> dim_campaign

staging.transactions + staging.transaction_items --->> fact_sales
```

## 3. Data Model

### Source / Staging Tables

Data source yang digunakan dalam project ini disimpan pada PostgreSQL schema `staging`.

Terdapat lima tabel utama:

| Tabel | Kolom Utama | Deskripsi |
|---|---|---|
| `customers` | `customer_id` | Data customer |
| `products` | `product_id` | Data product |
| `transactions` | `transaction_id`,`product_id` | Header transaksi dan id customer |
| `transaction_items` | `transaction_item_id`, `transaction_id`, `product_id` | Detail item dalam transaksi |
| `marketing_campaigns` | `campaign_id` | Data campaign marketing |


## 4. Project Structure

Struktur repository dirancang untuk memisahkan source data, pipeline orchestration, SQL transformation, diagram, dan konfigurasi project.

```text
.
├── dags/
│   ├── common/
│   │   ├── ingestion.py
│   ├── ingestion_master.py
│   ├── ingestion_transaction.py
│   ├── ingestion_transaction_item.py
│   ├── dim_customer_dag.py
│   ├── dim_product_dag.py
│   ├── dim_date_dag.py
│   ├── dim_campaign_dag.py
│   └── fact_sales_dag.py
│
├── data/
│   └── sample/
│       ├── customers.csv
│       ├── products.csv
│       ├── transactions.csv
│       ├── transaction_items.csv
│       └── marketing_campaigns.csv
│
├── sql/
│   ├── dwh/
│   │   ├── 01_dim_customer.sql
│   │   ├── 02_dim_product.sql
│   │   ├── 03_dim_date.sql
│   │   ├── 04_dim_campaign.sql
│   │   └── 05_fact_sales.sql
│   │
│   └── staging/
│       └── create_staging.sql
│
├── .env
├── .gitignore
├── docker-compose.yaml
├── makefile
├── README.md
└── requirements.txt
```

## 5. Prerequisites

### Software Requirements

Sebelum menjalankan project, pastikan software berikut telah tersedia:

- Git
- Docker
- Docker Compose
- Python 3.14
- Dbeaver client (opsional, untuk melakukan koneksi dan validasi database secara langsung)

Docker digunakan untuk menjalankan environment PostgreSQL dan Apache Airflow, sedangkan Python digunakan untuk proses ETL dan script pendukung.

### Python Requirements

Project menggunakan Python 3.14.

Python dependencies didefinisikan pada: `requirements.txt` >> `pip install -r requirements.txt`
