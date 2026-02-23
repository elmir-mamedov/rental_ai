import httpx
from lxml import html

url = "https://www.bezrealitky.cz/nemovitosti-byty-domy/985097-nabidka-pronajem-nebytoveho-prostoru-wetzlar"
url2 = 'https://www.bezrealitky.cz/nemovitosti-byty-domy/992792-nabidka-pronajem-pozemku-jiriho-z-podebrad-ceske-budejovice'
r = httpx.get(url2)
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


print(f"Title: {title}")
print(f"Price: {price[0]}")
print(f"Location: {location}")
print(f"Description in English: {description_EN}")
print(f"Description in Czech: {description_clean_native}")

