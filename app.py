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


async def fetch(session, url: str) -> str:
    """Fetch an URL async.

    Args:
        session (aiohttp.ClientSession): An aiohttp Client Session.
        url (str): URL

    Returns:
        str: Page text response.
    """
    async with session.get(url) as response:
        return await response.text()


async def fetch_all(urls: list) -> list:
    """Fetch a list of urls in async mode.

    Args:
        urls (list): List of URLs

    Returns:
        list: List of responses as text.
    """
    async with aiohttp.ClientSession() as session:
        responses = await asyncio.gather(*[
            fetch(session, url)
            for url in urls
        ])
        return responses


def parse_pages(home_page: str) -> list:
    """According to Comper home-page, it will find 6 product's URL on that.

    Args:
        home_page (str): Comper home-page to find products.

    Returns:
        list: List of products URLs.
    """
     
    regex = re.compile(ITEMS_REGEX, flags=re.MULTILINE)
    items = re.findall(regex, home_page)
    item_regex = re.compile(ITEM_URL_REGEX)
    urls = [f"{re.findall(item_regex, item)[0]}?sc={DF_DIG}" for item in items]
    items_response = asyncio.run(fetch_all(urls[:6]))
    
    items_page_text = [
        {'text': item, 'url': url} 
        for item, url in zip(items_response, urls) if not re.search(PAGE_ERROR, item)
    ]    
    
    return items_page_text


def make_items_data(items_page_text: list) -> list:
    """Read the page's data layer and get important info to compose a products list.

    Args:
        items_page_text (list): Products page list as text.

    Returns:
        list: Products info list.
    """
    items_data = []
    
    for item_page in items_page_text:
        data_layer = json.loads(re.findall(DATA_LAYER_REGEX, item_page['text'])[0])
        items_data.append({
            "name": data_layer["name"],
            "img_url": data_layer["skus"][0]["image"],
            "price": data_layer["skus"][0]["bestPrice"]/100 if data_layer["skus"][0]["available"] else 0,
            "availability": data_layer["skus"][0]["available"],
            "url": item_page["url"].replace(f"?sc={DF_DIG}", "")        
        })
    
    return items_data


if __name__ == '__main__':
    home_page = asyncio.run(fetch_all([HOME_URL]))[0]
    items_page_text = parse_pages(home_page)
    items_data = make_items_data(items_page_text)
    
    with open('output.json', 'w') as f:
        f.write(json.dumps(items_data[:3]))
        f.close()
