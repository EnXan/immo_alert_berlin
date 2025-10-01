import asyncio
import json
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, JsonCssExtractionStrategy
from crawl4ai import DefaultMarkdownGenerator, PruningContentFilter

async def crawl():
    url_list = await crawl_list()
    property_list = await crawl_properties(url_list)
    return property_list



async def crawl_properties(url_list: list):

    css_strategy = JsonCssExtractionStrategy(schema={
    "name": "www.howoge.de Schema",
    "baseSelector": "body",
    "fields": [
        {
        "name": "title",
        "selector": "#main > div.ce-wrapper.flat-detail__stage.background-color-petrol-brighter > div > div.data > h1",
        "type": "text"
        },
        {
        "name": "address",
        "selector": "#main > div.ce-wrapper.flat-detail__stage.background-color-petrol-brighter > div > div.data > div > p",
        "type": "text"
        },
        {
        "name": "price",
        "selector": "#main > div.ce-wrapper.flat-detail__stage.background-color-petrol-brighter > div > div.data > dl > div:nth-child(1) > dd",
        "type": "text"
        },
        {
        "name": "rooms",
        "selector": "#main > div.ce-wrapper.flat-detail__stage.background-color-petrol-brighter > div > div.data > dl > div:nth-child(3) > dd",
        "type": "text"
        },
        {
        "name": "size",
        "selector": "#main > div.ce-wrapper.flat-detail__stage.background-color-petrol-brighter > div > div.data > dl > div:nth-child(2) > dd",
        "type": "text"
        },
        {
        "name": "wbs_required",
        "selector": "N.A.",
        "type": "text"
        }
    ]
    })

    config = CrawlerRunConfig(
        extraction_strategy=css_strategy,
        verbose=True,
        markdown_generator=DefaultMarkdownGenerator(
                content_filter=PruningContentFilter()
        ),
    )

    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun_many(
            urls=url_list,
            bypass_cache=True,
            verbose=True,
            config=config
        )
    
    all_properties = []
    
    for result in results:
        if result.success:

            data = json.loads(result.extracted_content)
            if data and isinstance(data, list) and len(data) > 0:
                property_info = data[0]
                property_info["url"] = result.url
                
                # Bereinige alle Text-Felder von Whitespace
                for key, value in property_info.items():
                    if isinstance(value, str):
                        # Entferne \n, \t, überflüssige Leerzeichen
                        property_info[key] = ' '.join(value.split())
                
                # Filter für max. 900€ Miete
                price_text = property_info.get('price', '').strip()
                if price_text:
                    try:
                        # Extrahiere Zahl aus dem Text (z.B. "850,50 €" -> 850.50)
                        import re
                        price_match = re.search(r'([0-9,.]+)', price_text.replace(',', '.'))
                        if price_match:
                            price_number = float(price_match.group(1))
                            if price_number <= 900:
                                all_properties.append(property_info)
                        else:
                            # Wenn keine Zahl gefunden wird, trotzdem hinzufügen
                            all_properties.append(property_info)
                    except (ValueError, AttributeError):
                        # Bei Fehlern trotzdem hinzufügen
                        all_properties.append(property_info)
                else:
                    # Wenn keine Preis-Info vorhanden ist, trotzdem hinzufügen
                    all_properties.append(property_info)
        else:
            print(f"Fehler bei {result.url}: {result.error_message}")
    
    return all_properties


async def crawl_list():
    css_strategy = JsonCssExtractionStrategy(schema={
        "baseSelector": "div.content > div.address",
        "fields": [{"name": "link","selector": "a.flat-single--link","type": "attribute","attribute": "href"}]
    })
    
    all_links = set()

    js_filter_interaction = """
    // Wait for page to load
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // 1. Click on 2 rooms filter
    const roomsButton = document.querySelector('#rooms-2');
    if (roomsButton) {
        roomsButton.click();
        await new Promise(resolve => setTimeout(resolve, 500));
    }
    
    // 2. Click the search submit button
    const searchSubmitButton = document.querySelector('#flat-search-filter--form > div.container > div.filters > div > div.col-12.col-lg-2.col__submit.d-flex.align-items-end > button');
    if (searchSubmitButton) {
        searchSubmitButton.click();
    }
    
    // Wait for search results to load
    await new Promise(resolve => setTimeout(resolve, 3000));
    """
    
    async with AsyncWebCrawler(config=BrowserConfig(headless=True)) as crawler:
        # Erste Seite
        result = await crawler.arun(
            url="https://www.howoge.de/immobiliensuche/wohnungssuche.html",
            config=CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                extraction_strategy=css_strategy,
                js_code=js_filter_interaction,
                session_id="session",
                wait_for="#immoobject-list-2 > div"
            )
        )
        
        if result.success:
            for prop in json.loads(result.extracted_content):
                all_links.add(prop.get('link'))

    all_urls = []
    
    for link in all_links:
        all_urls.append(f"https://www.howoge.de/{link}" if not link.startswith('http') else link)

    return all_urls

if __name__ == "__main__":
    asyncio.run(crawl())