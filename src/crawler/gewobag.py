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
    "name": "www.gewobag.de Schema",
    "baseSelector": "body",
    "fields": [
        {
        "name": "title",
        "selector": "div > header.entry-header > h1.entry-title",
        "type": "text"
        },
        {
        "name": "address",
        "selector": "#rental-overview > div.overview-details > table.overview-table.details-general > tbody > tr:nth-child(1) > td",
        "type": "text"
        },
        {
        "name": "price",
        "selector": "#rental-overview > div.overview-details > table.overview-table.details-price > tbody > tr.interest > td",
        "type": "text"
        },
        {
        "name": "rooms",
        "selector": "#rental-overview > div.overview-details > table.overview-table.details-general > tbody > tr:nth-child(5) > td",
        "type": "text"
        },
        {
        "name": "size",
        "selector": "#rental-overview > div.overview-details > table.overview-table.details-general > tbody > tr:nth-child(6) > td",
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
                
                all_properties.append(property_info)
        else:
            print(f"Fehler bei {result.url}: {result.error_message}")
    
    return all_properties


async def crawl_list():
    css_strategy = JsonCssExtractionStrategy(schema={
        "baseSelector": "article.angebot-big-box > div.angebot-content > div.angebot-footer",
        "fields": [{"name": "link","selector": "a.read-more-link","type": "attribute","attribute": "href"}]
    })
    
    all_links = set()

    js_filter_interaction = """
    // Wait for page to load
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // 1. Click the rental options dialog button
    const dialogButton = document.querySelector('#rental-options-dialog-button');
    if (dialogButton) {
        dialogButton.click();
        await new Promise(resolve => setTimeout(resolve, 1000));
    }
    
    // 2. Fill max rent field with 900
    const maxRentInput = document.querySelector('#gesamtmiete_bis');
    if (maxRentInput) {
        maxRentInput.focus();
        maxRentInput.value = '900';
        maxRentInput.dispatchEvent(new Event('input', { bubbles: true }));
        maxRentInput.dispatchEvent(new Event('change', { bubbles: true }));
        await new Promise(resolve => setTimeout(resolve, 300));
    }
    
    // 3. Fill rooms from field with 2
    const roomsFromInput = document.querySelector('#zimmer_von');
    if (roomsFromInput) {
        roomsFromInput.focus();
        roomsFromInput.value = '2';
        roomsFromInput.dispatchEvent(new Event('input', { bubbles: true }));
        roomsFromInput.dispatchEvent(new Event('change', { bubbles: true }));
        await new Promise(resolve => setTimeout(resolve, 300));
    }
    
    // 4. Fill rooms to field with 3
    const roomsToInput = document.querySelector('#zimmer_bis');
    if (roomsToInput) {
        roomsToInput.focus();
        roomsToInput.value = '3';
        roomsToInput.dispatchEvent(new Event('input', { bubbles: true }));
        roomsToInput.dispatchEvent(new Event('change', { bubbles: true }));
        await new Promise(resolve => setTimeout(resolve, 300));
    }
    
    // 5. Click the search submit button
    const searchSubmitButton = document.querySelector('#search-submit');
    if (searchSubmitButton) {
        searchSubmitButton.click();
    }
    
    // Wait for search results to load
    await new Promise(resolve => setTimeout(resolve, 3000));
    """
    
    async with AsyncWebCrawler(config=BrowserConfig(headless=True)) as crawler:
        # Erste Seite
        result = await crawler.arun(
            url="https://www.gewobag.de/fuer-mietinteressentinnen/mietangebote/?objekttyp%5B%5D=wohnung&gesamtmiete_von=&gesamtmiete_bis=&gesamtflaeche_von=&gesamtflaeche_bis=&zimmer_von=&zimmer_bis=&sort-by=",
            config=CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                extraction_strategy=css_strategy,
                js_code=js_filter_interaction,
                session_id="session",
                wait_for="css:article.angebot-big-box"
            )
        )
        
        if result.success:
            for prop in json.loads(result.extracted_content):
                all_links.add(prop.get('link'))

    all_urls = []
    
    for link in all_links:
        all_urls.append(f"https://www.gewobag.de/{link}" if not link.startswith('http') else link)

    return all_urls

if __name__ == "__main__":
    asyncio.run(crawl())