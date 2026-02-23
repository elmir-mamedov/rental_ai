"""collect_urls.py
Collect listing URLs from Bezrealitky and store them in the database queue.
"""
import asyncio
from db import get_connection
from sitemap import fetch_xml, parse_sitemap
from db import insert_url

SITEMAP_URL = "https://www.bezrealitky.cz/sitemap/sitemap.xml"

async def collect():
    # Fetch main sitemap XML
    xml = await fetch_xml(SITEMAP_URL)
    urls = parse_sitemap(xml)

    # If sitemap index (links to other sitemaps), fetch each child sitemap
    if urls and urls[0].endswith(".xml"):
        all_urls = []
        for sitemap_url in urls:
            sub_xml = await fetch_xml(sitemap_url)
            sub_urls = parse_sitemap(sub_xml)
            all_urls.extend(sub_urls)
        urls = all_urls

    print(f"Discovered {len(urls)} URLs")

    # Insert URLs into url_queue

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany(
                """
                INSERT INTO url_queue (url)
                VALUES (%s)
                ON CONFLICT (url) DO NOTHING;
                """,
                [(url,) for url in urls]
            )
            inserted = cur.rowcount
        conn.commit()

    print(f"Inserted {inserted} new URLs.")


if __name__ == "__main__":
    asyncio.run(collect())
