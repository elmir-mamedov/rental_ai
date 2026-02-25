# db.py
import os
import psycopg # popular PostgreSQL adapter for the Python.
from psycopg.rows import dict_row
from dotenv import load_dotenv

# Load .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Connect to PostgreSQL
def get_connection():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)

# Initialize database: create tables if they don't exist
def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS listings (
                id SERIAL PRIMARY KEY,
                url TEXT UNIQUE NOT NULL,
                title TEXT,
                price INTEGER,
                currency TEXT,
                location TEXT,
                description_en TEXT,
                description_native TEXT,
            
                construction_of_building TEXT,
                condition TEXT,
                equipped TEXT,
                area_of_property TEXT,
                usable_area TEXT,
                floor TEXT,
                disposition TEXT,
                ownership TEXT,
                city_location TEXT,
                age TEXT,
            
                garage BOOLEAN,
                elevator BOOLEAN,
                balcony BOOLEAN,
                parking BOOLEAN,
                barrier_free_access BOOLEAN,
                cellar BOOLEAN,
                near_public_transport BOOLEAN,
                terrace BOOLEAN,
            
                created_at TIMESTAMP DEFAULT NOW()
            );
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS url_queue (
                    url TEXT PRIMARY KEY,
                    processed BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT NOW()
                );
                """)
            conn.commit()


    print("Databases initialized ✅")




# Insert a new listing
'''Stores all scraped property listings (URL, title, price, location, description, etc.).'''
def insert_listing(url, title=None, price=None, currency=None, location=None,
                   description_en=None,
                   description_native=None,
                   construction_of_building=None,
                   condition=None,
                   equipped=None,
                   area_of_property=None,
                   usable_area=None,
                   floor=None,
                   disposition=None,
                   ownership=None,
                   city_location=None,
                   age=None,
                   garage=None,
                   elevator=None,
                   balcony=None,
                   parking=None,
                   barrier_free_access=None,
                   cellar=None,
                   near_public_transport=None,
                   terrace=None,
                   ):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO listings (url, title, price, currency, location, description_en, description_native,\
            construction_of_building, condition, equipped, area_of_property, usable_area, floor, disposition, \
            ownership, city_location, age, garage, elevator, balcony, parking, barrier_free_access, cellar, \
            near_public_transport, terrace)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (url) DO NOTHING
            RETURNING id;
            """, (url, title, price, currency, location, description_en, description_native,
            construction_of_building, condition, equipped, area_of_property, usable_area, floor, disposition,
            ownership, city_location, age, garage, elevator, balcony, parking, barrier_free_access, cellar,
            near_public_transport, terrace))
            listing_id = cur.fetchone()
            conn.commit()
            return listing_id

# db.py (add below your existing functions)

def insert_url(url: str):
    """Insert a URL into the queue if it doesn't exist yet."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO url_queue (url)
                VALUES (%s)
                ON CONFLICT (url) DO NOTHING;
                """,
                (url,)
            )
        conn.commit()


def get_unprocessed_urls(limit=50):
    """Get a batch of unprocessed URLs from the queue."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT url FROM url_queue
                WHERE processed = FALSE
                ORDER BY created_at
                LIMIT %s;
                """,
                (limit,)
            )
            urls = [row['url'] for row in cur.fetchall()]
    return urls


def mark_url_processed(url: str):
    """Mark a URL as processed."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE url_queue SET processed = TRUE WHERE url = %s;",
                (url,)
            )
        conn.commit()
