import asyncio
from db import get_connection, init_db
from sitemap import fetch_xml, parse_sitemap

SITEMAP_URL = "https://www.bezrealitky.cz/sitemap/sitemap.xml"


async def collect():
    init_db()

    xml = await fetch_xml(SITEMAP_URL)
    urls = parse_sitemap(xml)

    # If sitemap index → fetch children
    if urls and urls[0].endswith(".xml"):
        all_urls = []
        for sitemap_url in urls:
            sub_xml = await fetch_xml(sitemap_url)
            sub_urls = parse_sitemap(sub_xml)
            all_urls.extend(sub_urls)
        urls = all_urls

    print(f"Discovered {len(urls)} URLs")

    with get_connection() as conn:
        with conn.cursor() as cur:
            for url in urls:
                cur.execute(
                    """
                    INSERT INTO url_queue (url)
                    VALUES (%s)
                    ON CONFLICT (url) DO NOTHING;
                    """,
                    (url,)
                )
        conn.commit()

    print("Inserted into database.")


if __name__ == "__main__":
    asyncio.run(collect())
