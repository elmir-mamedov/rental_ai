# CZ Real Estate Scraper

🏠  – Central Europe Real Estate Scraper & Database

This project collects real estate listings from Bezrealitky and stores structured data in PostgreSQL for further analysis and modeling (EDA, price modeling, recommendation systems, etc.).

It is designed as a scalable scraping pipeline with a URL queue and structured relational storage.

📦 Project Structure
bezrealitky_scraper/\
|\
|── db.py                     # Database schema + insert logic  \
|── scrape_listings_sync.py   # Synchronous scraper             \
|── collect_urls.py           # URL collector (seed stage)      \
|── sitemap.py                # Sitemap URL extractor           \
|── listings.csv              # Exported data (optional)        \
|── test_scripts/             # Experiments / debugging         \
|── docs/

## 🗄 Database Schema

Two tables are used:

### 1️⃣ listings

Stores structured property data.

Main fields:

- url (unique)

- title

- price

- currency

- location

- description_en

- description_native

Property details:

- construction_of_building

- condition

- equipped

- area_of_property

- usable_area

- floor

- disposition

- ownership

- city_location

- age

Boolean features:

- garage

- elevator

- balcony

- parking

- barrier_free_access

- cellar

- near_public_transport

- terrace

Metadata:

- created_at

### 2️⃣ url_queue

Implements queue-based scraping.

- url

- processed

- created_at

This prevents duplicate scraping and allows batch processing.

## ⚙️ Setup
#### 1️⃣ Create virtual environment
python -m venv .venv
source .venv/bin/activate

#### 2️⃣ Install dependencies
pip install psycopg[binary] httpx lxml python-dotenv

#### 3️⃣ Configure environment variables

Create .env:

DATABASE_URL=postgresql://user:password@localhost:5432/cz_real_estate

##### 4️⃣ Initialize database
from db import init_db
init_db()


This creates both tables if they don’t exist.

## 🌐 Scraping Pipeline
#### Step 1 – Collect URLs

Use:

collect_urls.py

These insert URLs into url_queue.

#### Step 2 – Scrape Listings

Run:

python scrape_listings_sync.py


### The scraper:

Fetches unprocessed URLs

- Extracts:

  - Title

  - Price + currency

  - Location

  - Descriptions (EN + native)
    
  - Key-value table attributes
    
  - Boolean icon-based features

- Inserts into listings

- Marks URL as processed

- Batch size is configurable via:

Maybe reduce BATCH_SIZE for test runs.

## 📊 Exporting Data

From PostgreSQL:

\copy (SELECT * FROM listings) TO 'listings.csv' WITH (FORMAT csv, HEADER true);


Use listings.csv for EDA or modeling.

## 🧪 EDA

Example notebook: eda_listings.ipynb

## 🚧 Known Limitations

JavaScript-rendered fields are not supported (static scraping only).

Some table keys may vary in naming.

Some listings may lack certain attributes.

No async / parallelization yet.

No rate limiting implemented.

## 🔮 Future Improvements

Async scraping (httpx async or asyncio)

Switch to SQLAlchemy

More robust scraping logic

Better normalization (maybe diacritics removal)

Image scraping