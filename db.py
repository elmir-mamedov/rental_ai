import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg.connect(DATABASE_URL)

def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS url_queue (
                    url TEXT PRIMARY KEY,
                    status TEXT DEFAULT 'pending',
                    discovered_at TIMESTAMP DEFAULT NOW(),
                    last_attempt TIMESTAMP,
                    error TEXT
                );
            """)
        conn.commit()
