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
Source Data (dummy CSV files)
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

## 6. Setup

Bagian ini menjelaskan langkah-langkah untuk menyiapkan environment lokal sebelum menjalankan data pipeline.

### 6.1 Clone Repository

Clone repository project ke local environment:

```bash
git clone https://github.com/ardfahriarr/airflow-dwh-project.git
cd airflow-dwh-project
```

Pastikan struktur utama repository tersedia:

```text
airflow-dwh-project/
├── config/
├── dags/
├── data/
├── plugins/
├── scripts/
├── sql/
├── .env.example
├── docker-compose.yaml
├── makefile
└── requirements.txt
```

```bash
git pull
```

---

### 6.2 Environment Variables

Project menggunakan environment variables untuk menyimpan konfigurasi runtime dan informasi koneksi yang tidak sebaiknya ditulis langsung di source code.

Buat file `.env` berdasarkan template yang tersedia di makefile:

```bash
make env
```

Kemudian sesuaikan nilai variable di dalam `.env` dengan local environment.

Contoh:

```env
AIRFLOW_UID=<your_linux_user_id>

# Airflow Web User
_AIRFLOW_WWW_USER_CREATE=true
_AIRFLOW_WWW_USER_USERNAME=admin
_AIRFLOW_WWW_USER_PASSWORD=<generated_by_cryptography_library>

# Airflow Fernet Key
AIRFLOW__CORE__FERNET_KEY=<generated_by_cryptography_library>
```

---

### 6.3 Python Environment

Python virtual environment digunakan untuk mengisolasi dependency project dari system Python.

Virtual environment sudah otomatis tergenerate dengan menjalankan perintah make env sebelumnya

Aktifkan virtual environment:

#### Linux / macOS

```bash
source .venv/bin/activate
```

#### Windows

```powershell
.venv\Scripts\activate
```

Setelah aktif, upgrade `pip`:

```bash
python -m pip install --upgrade pip
```

Pastikan Python yang digunakan berasal dari virtual environment:

```bash
which python
```

atau:

```bash
python --version
```

Contoh:

```text
Python 3.x.x
```

---

### 6.4 Install Dependencies

Install seluruh Python dependency yang digunakan oleh project:

```bash
pip install -r requirements.txt
```

Untuk memastikan dependency telah ter-install:

```bash
pip list
```

Dependency project mencakup library yang dibutuhkan untuk:

- Apache Airflow
- PostgreSQL connectivity
- Python-based ETL
- Data processing
- Data validation
- Utility scripts

Jika menggunakan virtual environment, pastikan environment tersebut sudah aktif sebelum menjalankan command instalasi.

Untuk memverifikasi Airflow:

```bash
airflow version
```

---

### 6.5 Airflow Setup

Airflow digunakan sebagai orchestration layer untuk menjalankan dan mengatur dependency antar proses ETL.

Pastikan environment variables yang dibutuhkan Airflow sudah tersedia sebelum melakukan initialization.

Jika menggunakan Docker Compose, build dan start service:

```bash
docker compose up -d
```

Periksa seluruh service:

```bash
docker compose ps
```

Untuk melihat log Airflow:

```bash
docker compose logs -f airflow-apiserver
```

Jika menggunakan service Airflow yang berbeda pada `docker-compose.yaml`, gunakan nama service yang sesuai dengan compose configuration.

#### Initialize Airflow Database

Sebelum Airflow digunakan untuk pertama kali, metadata database perlu diinisialisasi atau dimigrasikan:

```bash
docker compose run --rm airflow-init
```

Jika project menggunakan initialization command yang berbeda pada `makefile`, command tersebut dapat digunakan sebagai alternatif:

```bash
make airflow-init
```

Kemudian setelah selesai, run docker-compose.yaml dengan perintah:

```
make up
```

Setelah initialization selesai, pastikan service Airflow berjalan:

```bash
docker compose ps
```

Kemudian akses Airflow UI melalui:

```text
http://localhost:8080
```

Login menggunakan credential Airflow yang dikonfigurasi pada environment/project setup.

#### Verify DAGs

Setelah Airflow berjalan, DAG yang terdapat pada directory:

```text
dags/
```

akan diproses oleh Airflow.

DAG dapat diverifikasi melalui Airflow UI atau menggunakan CLI:

```bash
airflow dags list
```

Pastikan DAG project muncul pada daftar tersebut.

---

### 6.6 Database Connection

Airflow membutuhkan database connection untuk dapat berkomunikasi dengan PostgreSQL yang digunakan sebagai target Data Warehouse.

Connection dapat dikonfigurasi melalui Airflow UI:

```text
Admin → Connections
```

Buat connection dengan parameter yang sesuai dengan PostgreSQL configuration.

Contoh:

```text
Connection ID : postgres_dwh
Connection Type: PostgreSQL
Host          : postgres
Port          : 5432
Database      : airflow_dwh
Username      : airflow
Password      : airflow
```

> Jika Airflow berjalan di dalam Docker Compose dan PostgreSQL juga berjalan sebagai service di dalam Docker Compose network, gunakan nama service PostgreSQL sebagai `Host`, bukan `localhost`.

Contoh:

```text
Host: postgres
```

Sedangkan apabila koneksi dilakukan dari host machine secara langsung:

```text
Host: localhost
```

---

### Setup Summary

Secara keseluruhan, urutan setup adalah:

```text
1. Clone Repository
2. Create .env
3. Create Python Virtual Environment
4. Install Dependencies
5. Initialize and run Airflow
6. Verify Airflow DAGs
7. Configure PostgreSQL Connection
8. Environment Ready
```

Setelah seluruh langkah di atas berhasil, environment siap digunakan untuk menjalankan tahap **Data Preparation** dan **ETL Pipeline**.

## 7. Data Preparation

Tahap Data Preparation digunakan untuk menyiapkan synthetic source data dan struktur staging database sebelum pipeline ETL dijalankan menggunakan Apache Airflow.

Proses ini terdiri dari tiga tahap utama:

```text
Data Generation
      ▼
Create Staging Tables
      ▼
Airflow Ingestion
```

### 7.1 Generate Sample Data

Source data pada project ini merupakan synthetic data yang dibuat menggunakan Jupyter Notebook:

```text
scripts/data_generator.ipynb
```

Notebook digunakan untuk menghasilkan dataset yang merepresentasikan data operasional yang akan diproses oleh pipeline.

Jalankan notebook:

```text
scripts/data_generator.ipynb
```

Setelah proses generation selesai, file CSV akan tersedia pada:

```text
data/sample/
```

Struktur sample data:

```text
data/sample/
├── customers.csv
├── marketing_campaigns.csv
├── products.csv
├── transaction_items.csv
└── transactions.csv
```

Dataset tersebut kemudian digunakan sebagai source untuk proses ingestion ke staging database.

> Synthetic data digunakan agar pipeline dapat dijalankan secara reproducible tanpa bergantung pada external data source.

---

### 7.2 Create Staging Tables

Setelah sample data tersedia, tahap berikutnya adalah membuat struktur tabel staging pada PostgreSQL.

DDL staging tersedia pada:

```text
sql/staging/create_staging.sql
```

Jalankan SQL tersebut pada database PostgreSQL:

```sql
\i sql/staging/create_staging.sql
```

Atau file tersebut dapat dijalankan melalui database client seperti DBeaver.

Staging layer digunakan sebagai intermediate layer untuk menyimpan data hasil ingestion sebelum dilakukan transformation ke Data Warehouse.

Secara konseptual:

```text
CSV Source
    ▼
PostgreSQL Staging
    ▼
DWH Transformation
```

Staging table dibuat terlebih dahulu agar Airflow ingestion pipeline memiliki target table yang telah tersedia.

---

### 7.3 Load Data into Staging

Setelah staging tables berhasil dibuat, proses loading data dilakukan menggunakan Apache Airflow.

Tidak terdapat script Python terpisah untuk melakukan loading staging secara manual. Proses ingestion dikelola oleh Airflow DAG yang tersedia pada directory:

```text
dags/
```

DAG yang berkaitan dengan proses ingestion antara lain:

```text
dags/
├── ingestion.py
├── ingestion_master.py
├── ingestion_transaction.py
└── ingestion_transaction_item.py
```

Airflow bertanggung jawab untuk membaca source CSV dan melakukan proses ingestion ke staging table.

Secara umum:

```text
data/sample/*.csv
        ▼
Airflow Ingestion DAG
        ▼
PostgreSQL Staging
```

Setelah ingestion selesai, jumlah record pada staging dapat diperiksa menggunakan query:

```sql
SELECT COUNT(*)
FROM <staging_table>;
```

Sample data juga dapat diperiksa menggunakan:

```sql
SELECT *
FROM <staging_table>
LIMIT 10;
```

---

### 7.4 Source Data Validation

Validasi dilakukan untuk memastikan source data telah tersedia dan staging table berhasil menerima data sebelum proses Data Warehouse dijalankan.

Validasi mencakup:

- File source tersedia.
- Struktur source data sesuai dengan expected schema.
- Staging table tersedia.
- Data berhasil di-load ke staging.
- Jumlah record dapat diverifikasi.
- Tidak terdapat masalah pada mandatory field yang dibutuhkan oleh transformation.

Validasi jumlah record dapat dilakukan dengan membandingkan source data dengan staging:

```text
CSV Row Count
      │
      │ compare
      ▼
Staging Row Count
```

Jika hasil ingestion tidak sesuai dengan expected result, proses Data Warehouse sebaiknya tidak dilanjutkan sebelum masalah tersebut diperbaiki.

---

## 8. ETL Pipeline

ETL pipeline menggunakan Apache Airflow sebagai orchestration layer.

Pipeline dibagi menjadi dua kelompok proses utama:

```text
                    STAGING
             ┌─────────┴─────────┐       
             ▼                   ▼
       INGESTION             DWH ETL       
             ▼                   ▼
      Staging Tables      Dimension Tables
                                 ▼
                            Fact Table
```

Ingestion bertanggung jawab untuk memindahkan data dari CSV source ke staging database, sedangkan DWH ETL bertanggung jawab untuk melakukan transformation dan loading ke Data Warehouse.

---

### 8.1 DAG Overview

DAG yang digunakan dalam project berada pada directory:

```text
dags/
```

Struktur DAG utama:

```text
dags/
├── ingestion.py
├── ingestion_master.py
├── ingestion_transaction.py
├── ingestion_transaction_item.py
│
├── dim_customer_dag.py
├── dim_product_dag.py
├── dim_date_dag.py
├── dim_campaign_dag.py
│
└── fact_sales_dag.py
```

Pipeline dibagi menjadi beberapa DAG agar setiap logical processing stage dapat dikelola dan dimonitor secara terpisah.

Secara umum:

```text
Source CSV
    ▼
Ingestion DAGs
    ▼
Staging
    ▼
Dimension DAGs
    ▼
Fact DAG
    ▼
Data Warehouse
```

---

### 8.2 Ingestion Pipeline

Ingestion pipeline bertanggung jawab untuk memuat source CSV ke staging database.

Proses ingestion terdiri dari beberapa DAG/task yang menangani kelompok data yang berbeda.

Secara konseptual:

```text
CSV SOURCE
- Master Ingestion
- Transaction Ingestion
- Transaction Item Ingestion
STAGING DB
```

File yang digunakan sebagai source:

```text
data/sample/
├── customers.csv
├── marketing_campaigns.csv
├── products.csv
├── transactions.csv
└── transaction_items.csv
```

Hasil dari proses ingestion adalah data yang tersedia pada staging database dan siap digunakan oleh proses transformation.

---

### 8.3 Dimension Pipelines

Setelah data tersedia pada staging, pipeline Data Warehouse melakukan proses loading dimension.

Dimension DAG yang tersedia:

```text
dim_customer_dag.py
dim_product_dag.py
dim_date_dag.py
dim_campaign_dag.py
```

Dimension tersebut menghasilkan:

```text
dim_customer
dim_product
dim_date
dim_campaign
```

SQL transformation untuk masing-masing dimension tersedia pada:

```text
sql/dwh/
├── 01_dim_customer.sql
├── 02_dim_product.sql
├── 03_dim_date.sql
└── 04_dim_campaign.sql
```
Dimension table harus tersedia terlebih dahulu karena fact table membutuhkan key dari dimension tersebut.

---

### 8.4 Fact Pipeline

Setelah dimension selesai diproses, pipeline berikutnya adalah loading fact table.

Fact pipeline menggunakan:

```text
dags/fact_sales_dag.py
```

Dengan SQL transformation:

```text
sql/dwh/05_fact_sales.sql
```

Target fact table:

```text
fact_sales
```

Secara umum prosesnya:

```text
Staging
   ▼
Dimension Mapping
   ▼
Business Transformation
   ▼
fact_sales
```

Fact table menggabungkan data transaksi dengan dimension yang relevan untuk menghasilkan data yang siap digunakan untuk analytical workload.

---

### 8.5 DAG Scheduling

Selama development dan testing, DAG dapat dijalankan secara manual melalui Airflow UI atau Airflow CLI.

Untuk melihat DAG yang tersedia:

```bash
airflow dags list
```

Untuk menjalankan DAG secara manual:

```bash
airflow dags trigger <dag_id>
```

Untuk melihat execution/run yang telah dilakukan:

```bash
airflow dags list-runs -d <dag_id>
```

Manual trigger digunakan selama development agar setiap tahap pipeline dapat diverifikasi secara individual.

Pada environment production, DAG dapat dijalankan berdasarkan schedule yang telah dikonfigurasi pada masing-masing DAG.

---

### 8.6 Dependency Management

Dependency digunakan untuk memastikan data diproses dalam urutan yang benar.

Secara logical, pipeline mengikuti urutan:

```text
Create Staging Tables
        ▼
Ingestion
        ▼
Staging Data Available
        ▼
Dimension Processing
        ▼
Fact Processing
        ▼
DWH Ready
```
---

Dengan demikian, responsibility setiap layer dapat dipisahkan sebagai berikut:

| Layer | Responsibility |
|---|---|
| `scripts/data_generator.ipynb` | Membuat synthetic source data |
| `data/sample/` | Menyimpan sample CSV |
| `sql/staging/` | Membuat struktur staging table |
| `dags/ingestion*.py` | Ingestion CSV ke staging |
| `dags/dim_*_dag.py` | Membentuk dimension |
| `dags/fact_sales_dag.py` | Membentuk fact table |
| `sql/dwh/` | SQL transformation dan DWH loading |
| PostgreSQL | Staging dan Data Warehouse storage |
| Apache Airflow | Orchestration, scheduling, dependency, dan monitoring |