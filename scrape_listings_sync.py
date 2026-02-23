# scrape_listings_sync.py
import httpx
from lxml import html
from db import get_unprocessed_urls, insert_listing, mark_url_processed
import re

BATCH_SIZE = 2000  # number of URLs to process per run

def scrape_listing(url):
    try:
        resp = httpx.get(url, timeout=30)
        resp.raise_for_status()
        tree = html.fromstring(resp.text)

        # --- Working XPaths from your tester ---
        # Title
        title_parts = tree.xpath('//h1//text()')
        title = " ".join(t.strip() for t in title_parts if t.strip())

        # Price
        price_xpath = '//div[contains(@class,"justify-content-between")]//strong[contains(@class,"h4 fw-bold")]//span/text()'
        price = tree.xpath(price_xpath)

        price_clean = None
        currency = None

        if price:
            raw_price = price[0].strip()

            # Detect currency
            if "€" in raw_price:
                currency = "EUR"
            elif "Kč" in raw_price:
                currency = "CZK"
            elif "$" in raw_price:
                currency = "USD"
            else:
                currency = "UNKNOWN"

            # Extract only digits
            digits = re.sub(r"[^\d]", "", raw_price)
            if digits:
                price_clean = int(digits)

        # Location
        location = tree.xpath('//h1/span[contains(@class,"text-grey-dark")]/text()')
        location_clean = location[0].strip() if location else None

        # Description in english
        description_parts_en = tree.xpath('//div[contains(@id,"english")]//p[contains(@class,"text-perex")]/text()')
        description_clean_en = "\n".join(d.strip() for d in description_parts_en if d.strip())

        # Description in native
        desc_native_1 = tree.xpath(
            '//div[contains(@id,"native")]//p[contains(@class,"text-perex")]/text()'
        )  # this is for normal written in native
        desc_native_2 = tree.xpath(
            '//div[contains(@id,"tabpane-cs")]//p[contains(@class,"text-perex")]/text()'
        )  # this is if description was translated to czech language by AI

        description_parts_native = desc_native_1 + desc_native_2

        description_clean_native = "\n".join(
            d.strip() for d in description_parts_native if d.strip()
        )

        # Insert into DB
        insert_listing(
            url=url,
            title=title,
            price=price_clean,
            currency=currency,
            location=location_clean,
            posted_date=None,  # you can later extract this if needed
            description_en=description_clean_en,
            description_native = description_clean_native
        )
        mark_url_processed(url)
        print("Scraped ✅", url)

    except Exception as e:
        print("Error scraping", url, e)

def get_unprocessed_count():
    """Get the total number of unprocessed URLs in the queue."""
    from db import get_connection

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS total FROM url_queue WHERE processed = FALSE;")
            row = cur.fetchone()
            return row["total"] if row else 0

def main():
    total_unprocessed = get_unprocessed_count()
    print("Total number of unprocessed URLs:", total_unprocessed)
    urls = get_unprocessed_urls(BATCH_SIZE)
    if not urls:
        print("No more URLs to process.")
        return

    for i, url in enumerate(urls, 1):
        if not url.startswith("https://www.bezrealitky.cz/nemovitosti-"):
            continue  # skip non-listings
        scrape_listing(url)
        processed = i
        remaining = len(urls) - i
        percent = (processed / len(urls)) * 100
        print(f"Progress: {processed}/{len(urls)} ({percent:.1f}%) - Remaining in batch: {remaining}")

    print(f"Batch done. {total_unprocessed - len(urls)} URLs left unprocessed in total.")

if __name__ == "__main__":
    main()
