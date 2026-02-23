# Rental AI – Data Issues Log

## 2026-02-22 – Initial EDA

### Missing posted_date
- Column exists but always NULL
- Root cause: not scraped
- Action: remove column until implemented

### Some of the listings are from thrid-party websites.
This usually have prices in EUR and if we go to
the link, we can see something like "More info" instead
of "Objednat prohlidku."

### Some listings have 0 EUR in their price.
These are the listings from third-party websites, where
the price is given on request.


### Missing description
Some listings actually don't have a description in any language.