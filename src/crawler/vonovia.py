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
    "name": "www.vonovia.de Schema",
    "baseSelector": "body",
    "fields": [
        {
        "name": "title",
        "selector": "body > div.template > div > div > div > div.estate-detail-page > div.real-estate-hero > div:nth-child(1) > div.content-card > div.content > div.headlines > h1",
        "type": "text"
        },
        {
        "name": "address",
        "selector": "body > div.template > div > div > div > div.estate-detail-page > div.real-estate-hero > div:nth-child(1) > div.wrapper > div > a > span",
        "type": "text"
        },
        {
        "name": "price",
        "selector": "body > div.template > div > div > div > div.estate-detail-page > div.container > main > div.side-left > div.real-estate-numbers > div:nth-child(2) > div > div > div > div",
        "type": "text"
        },
        {
        "name": "rooms",
        "selector": "body > div.template > div > div > div > div.estate-detail-page > div.container > main > div.side-left > div.real-estate-numbers > div:nth-child(5) > div > div > div > div",
        "type": "text"
        },
        {
        "name": "size",
        "selector": "body > div.template > div > div > div > div.estate-detail-page > div.container > main > div.side-left > div.real-estate-numbers > div:nth-child(3) > div > div > div > div",
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
                
                # Spezielle Bereinigung für Adresse (falls vorhanden)
                if 'address' in property_info and property_info['address']:
                    address = property_info['address']
                    # Standardisiere Adressformat
                    import re
                    # Komma vor Postleitzahl normalisieren
                    address = re.sub(r',\s*(\d{5})', r', \1', address)
                    property_info['address'] = address
                
                # Filter für 2-3 Zimmer UND max. 900€
                rooms_text = property_info.get('rooms', '').strip()
                price_text = property_info.get('price', '').strip()
                
                # Zimmer-Filter
                rooms_ok = False
                if rooms_text:
                    try:
                        # Extrahiere Zahl aus dem Text (z.B. "2 Zimmer" -> 2)
                        import re
                        rooms_match = re.search(r'([0-9,.]+)', rooms_text.replace(',', '.'))
                        if rooms_match:
                            rooms_number = float(rooms_match.group(1))
                            if 2 <= rooms_number <= 3:
                                rooms_ok = True
                    except (ValueError, AttributeError):
                        pass
                
                # Preis-Filter
                price_ok = False
                if price_text:
                    try:
                        # Extrahiere Zahl aus dem Text (z.B. "850,50 €" -> 850.50)
                        import re
                        price_match = re.search(r'([0-9,.]+)', price_text.replace(',', '.'))
                        if price_match:
                            price_number = float(price_match.group(1))
                            if price_number <= 900:
                                price_ok = True
                    except (ValueError, AttributeError):
                        pass
                
                # Nur hinzufügen wenn beide Filter erfüllt sind
                if rooms_ok and price_ok:
                    all_properties.append(property_info)
                elif not rooms_text and not price_text:
                    # Fallback: Wenn keine Daten vorhanden sind, trotzdem hinzufügen
                    all_properties.append(property_info)
        else:
            print(f"Fehler bei {result.url}: {result.error_message}")
    
    return all_properties


async def crawl_list():
    css_strategy = JsonCssExtractionStrategy(schema={
        "baseSelector": "div.headlines > h2.h4.headline",
        "fields": [{"name": "link", "selector": "a", "type": "attribute", "attribute": "href"}]
    })
    
    all_links = set()


    
    async with AsyncWebCrawler(config=BrowserConfig(headless=True)) as crawler:
        # Erste Seite
        result = await crawler.arun(
            url="https://www.vonovia.de/zuhause-finden/immobilien?rentType=miete&city=Berlin&lift=0&parking=0&cellar=0&immoType=wohnung&priceMax=700&minRooms=0&floor=Beliebig&bathtub=0&bathwindow=0&bathshower=0&furnished=0&kitchenEBK=0&toiletSeparate=0&disabilityAccess=egal&seniorFriendly=0&balcony=egal&garden=0&subsidizedHousingPermit=egal&scroll=true",
            config=CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                extraction_strategy=css_strategy,
                session_id="session",
                wait_for="css:.teaser-xl-container, .list-real-estate, .headlines"
            )
        )
        
        if result.success:
            for prop in json.loads(result.extracted_content):
                all_links.add(prop.get('link'))

    all_urls = []
    
    for link in all_links:
        all_urls.append(f"https://www.vonovia.de{link}" if not link.startswith('http') else link)

    return all_urls

if __name__ == "__main__":
    asyncio.run(crawl())