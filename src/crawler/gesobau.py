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
    "name": "www.gesobau.de Schema",
    "baseSelector": "body",
    "fields": [
        {
        "name": "title",
        "selector": "#main > article > header > div > div > section > div > div:nth-child(2) > div > h1",
        "type": "text"
        },
        {
        "name": "address",
        "selector": "#main > article > header > div > div > section > div > div:nth-child(2) > div > span",
        "type": "text"
        },
        {
        "name": "price",
        "selector": "#immoKosten > div > div > div:nth-child(1) > div:nth-child(1) > section > div > div.co__main > div > table > tbody > tr:nth-child(4) > td",
        "type": "text"
        },
        {
        "name": "rooms",
        "selector": "#immoKennzahlen > div > div > div > div:nth-child(1) > section > div > div.co__main > div > table > tbody > tr:nth-child(1) > td",
        "type": "text"
        },
        {
        "name": "size",
        "selector": "#immoKennzahlen > div > div > div > div:nth-child(1) > section > div > div.co__main > div > table > tbody > tr:nth-child(2) > td",
        "type": "text"
        },
        {
        "name": "wbs_required",
        "selector": "#immoKennzahlen > div > div > div > div:nth-child(1) > section > div > div.co__main > div > table > tbody > tr:nth-child(3) > td",
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
                
                all_properties.append(property_info)
        else:
            print(f"Fehler bei {result.url}: {result.error_message}")
    
    return all_properties


async def crawl_list():
    css_strategy = JsonCssExtractionStrategy(schema={
        "baseSelector": "h3.basicTeaser__title > span.basicTeaser__title__text",
        "fields": [{"name": "link","selector": "a","type": "attribute","attribute": "href"}]
    })
    
    all_links = set()

    js_filter_interaction = """
    // Wait for page to load
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // 1. Fill rooms field with 2
    const roomsInput = document.querySelector('#facetzimmer-input');
    if (roomsInput) {
        roomsInput.focus();
        roomsInput.value = '2';
        roomsInput.dispatchEvent(new Event('input', { bubbles: true }));
        roomsInput.dispatchEvent(new Event('change', { bubbles: true }));
        await new Promise(resolve => setTimeout(resolve, 500));
    }
    
    // 2. Fill warm rent field with 900
    const warmRentInput = document.querySelector('#facetwarmmiete-input');
    if (warmRentInput) {
        warmRentInput.focus();
        warmRentInput.value = '900';
        warmRentInput.dispatchEvent(new Event('input', { bubbles: true }));
        warmRentInput.dispatchEvent(new Event('change', { bubbles: true }));
        await new Promise(resolve => setTimeout(resolve, 500));
    }
    
    // Wait for form updates to process
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 3. Click the submit button
    const submitButton = document.querySelector('#submit-facets');
    if (submitButton) {
        submitButton.click();
    }
    
    // Wait for search results to load
    await new Promise(resolve => setTimeout(resolve, 2000));
    """
    
    async with AsyncWebCrawler(config=BrowserConfig(headless=True)) as crawler:
        # Erste Seite
        result = await crawler.arun(
            url="https://www.gesobau.de/mieten/wohnungssuche/",
            config=CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                extraction_strategy=css_strategy,
                js_code=js_filter_interaction,
                session_id="session",
                wait_for="css:.basicTeaser__content, .teaserList, #tx-solr-search"
            )
        )
        
        if result.success:
            for prop in json.loads(result.extracted_content):
                all_links.add(prop.get('link'))
        
        # Weitere Seiten
        for page in range(2, 11):
            result = await crawler.arun(
                url="https://www.gesobau.de/mieten/wohnungssuche/",
                config=CrawlerRunConfig(
                    cache_mode=CacheMode.BYPASS,
                    extraction_strategy=css_strategy,
                    session_id="session",
                    js_code="document.querySelector('#tx-solr-search > nav > ul > li:nth-child(2) > a')?.click()",
                    js_only=True,
                    wait_for="css:.basicTeaser__content, .teaserList, #tx-solr-search",
                )
            )
            
            if not result.success:
                break
                
            new_links = {p.get('link') for p in json.loads(result.extracted_content) if p.get('link')}
            if not new_links or new_links.issubset(all_links):
                break
            all_links.update(new_links)

    all_urls = []
    
    for link in all_links:
        all_urls.append(f"https://www.gesobau.de/{link}" if not link.startswith('http') else link)

    return all_urls

if __name__ == "__main__":
    asyncio.run(crawl())