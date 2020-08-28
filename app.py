import asyncio
import re
import json

import aiohttp


HOME_URL = "https://www.comperdelivery.com.br/"
ITEMS_REGEX = r"<h3 class=\"shelf-item__title\">.*\n(.*)\n.*</h3>"
ITEM_URL_REGEX = r"href=\"(.*)\" "
PAGE_ERROR = r'"pageUrl":"http://www.comperdelivery.com.br/Sistema/404"'
DATA_LAYER_REGEX = r"skuJson_0 = (.*});"

DF_DIG = 3
MS_DIG = 2
MT_DIG = 1


async def fetch(session, url: str):
    async with session.get(url) as response:
        return await response.text()


async def fetch_all(urls: list):
    async with aiohttp.ClientSession() as session:
        responses = await asyncio.gather(*[
            fetch(session, url)
            for url in urls
        ])
        return responses


if __name__ == '__main__':
    with open("home.html", 'r') as f:
        html = str(f.read())
        f.close()
    
    regex = re.compile(ITEMS_REGEX, flags=re.MULTILINE)
    items = re.findall(regex, html)
    item_regex = re.compile(ITEM_URL_REGEX)
    urls = [f"{re.findall(item_regex, item)[0]}?sc={DF_DIG}" for item in items]
    items_response = asyncio.run(fetch_all(urls[:6]))
    items_page_text = [
        {'page_text': item, 'url': url} 
        for item, url in zip(items_response, urls) if not re.search(PAGE_ERROR, item)
    ]    
    data = []    
    
    for item_page in items_page_text:
        data_layer = json.loads(re.findall(DATA_LAYER_REGEX, item_page['page_text'])[0])
        data.append({
            "name": data_layer["name"],
            "img_url": data_layer["skus"][0]["image"],
            "price": data_layer["skus"][0]["bestPrice"]/100,
            "availability": data_layer["skus"][0]["available"],
            "url": item_page["url"]            
        })
    
    print(data)