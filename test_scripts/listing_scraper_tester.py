import httpx
from lxml import html

url = "https://www.bezrealitky.cz/nemovitosti-byty-domy/985097-nabidka-pronajem-nebytoveho-prostoru-wetzlar"
url2 = 'https://www.bezrealitky.cz/nemovitosti-byty-domy/992792-nabidka-pronajem-pozemku-jiriho-z-podebrad-ceske-budejovice'
url3 = 'https://www.bezrealitky.cz/nemovitosti-byty-domy/994324-nabidka-pronajem-bytu-podebradska-praha'
url4 = 'https://www.bezrealitky.cz/nemovitosti-byty-domy/993734-nabidka-pronajem-bytu-krymska-praha'
url5 = 'https://www.bezrealitky.cz/nemovitosti-byty-domy/907812-nabidka-pronajem-bytu-vinohradska-praha'
url6 = 'https://www.bezrealitky.cz/nemovitosti-byty-domy/983818-nabidka-pronajem-bytu-komoranska-praha'
url7 = 'https://www.bezrealitky.cz/nemovitosti-byty-domy/993981-nabidka-pronajem-bytu-cakovicka-praha'
url8 = 'https://www.bezrealitky.cz/nemovitosti-byty-domy/989720-nabidka-prodej-domu-salzburg-stadtrand-sud'
url9 = 'https://www.bezrealitky.cz/nemovitosti-byty-domy/990171-nabidka-prodej-domu-lipno-nad-vltavou'
r = httpx.get(url9)
tree = html.fromstring(r.text)

price = tree.xpath(
    '//div[contains(@class,"justify-content-between")]'
    '//strong[contains(@class,"h4 fw-bold")]//span/text()'
)

title_parts = tree.xpath('//h1//text()')
title = " ".join(t.strip() for t in title_parts if t.strip())

location = tree.xpath('//h1/span[contains(@class,"text-grey-dark")]/text()')
location = location[0].strip() if location else None

description_parts_EN = tree.xpath(
    '//div[contains(@id,"english")]'
    '//p[contains(@class,"text-perex")]/text()'
)
description_EN = "\n".join(d.strip() for d in description_parts_EN if d.strip())

desc_native_1 = tree.xpath(
    '//div[contains(@id,"native")]//p[contains(@class,"text-perex")]/text()'
) # this is for normal written in native
desc_native_2 = tree.xpath(
    '//div[contains(@id,"tabpane-cs")]//p[contains(@class,"text-perex")]/text()'
) # this is if description was translated to czech language by AI

description_parts_native = desc_native_1 + desc_native_2

description_clean_native = "\n".join(
    d.strip() for d in description_parts_native if d.strip()
)

# ---- Key-Value Table Details ----
rows = tree.xpath('//table//tr')
details = {}

for row in rows:
    key_parts = row.xpath('.//th//span//text()')
    value_parts = row.xpath('.//td//span//text()')

    if key_parts and value_parts:
        key = key_parts[0].strip()
        value = " ".join(v.strip() for v in value_parts if v.strip())
        details[key] = value

# Normalize keys to lowercase for safe access
normalized_details = {k.strip().lower(): v for k, v in details.items()}

construction_of_building = normalized_details.get("konstrukce budovy")
condition = normalized_details.get("stav")
equipped = normalized_details.get("vybaveno")
area_of_the_property = normalized_details.get("plocha pozemku")
usable_area = normalized_details.get("užitná plocha")
floor = normalized_details.get("podlaží")
disposition = normalized_details.get("dispozice")
ownership = normalized_details.get("vlastnictví")
city_location = normalized_details.get("umístění")
age = normalized_details.get("stáří")

# ---- Print ----
print(f"Title: {title}")
print(f"Price: {price[0]}")
print(f"Location: {location}")
print(f"Description in English:\n{description_EN}\n")
print(f"Description in Czech:\n{description_clean_native}\n")
print(f"Konstrukce budovy: {construction_of_building}")
print(f"Stav: {condition}")
print(f"Vybaveno: {equipped}")
print(f"Uzitna plocha: {usable_area} m2")
print(f"Plocha pozemku: {area_of_the_property}")
print(f"Floor: {floor}")
print(f"Disposition: {disposition}")
print(f"Ownership: {ownership}")
print(f"City Location: {city_location}")
print(f"Age: {age}")

# --- Boolean features based on icons/text ---
boolean_features = {
    "garage": "Garáž",
    "elevator": "Výtah",
    "balcony": "Balkón",       # example
    "parking": "Parkování",
    "barrier-free_access": "Bezbariérový přístup",
    "cellar": "Sklep",
    "public_transport": "MHD",
    "terrace": "Terasa",
}

# Container of icon-based rows
icon_rows = tree.xpath('//div[contains(@class,"ParamsTable_paramsTable")]//tr')

# Initialize dictionary
features_dict = {key: False for key in boolean_features}

for row in icon_rows:
    # Check all text inside row
    text_in_row = " ".join(row.xpath('.//span/text()')).strip()
    for key, label in boolean_features.items():
        if label in text_in_row:
            features_dict[key] = True

# Example of printing
print('\n')
for k, v in features_dict.items():
    print(f"{k}: {v}")
