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
    "name": "www.wbm.de Schema",
    "baseSelector": "#maincontent",
    "fields": [
        {
        "name": "title",
        "selector": "section.openimmo-detail__header > div.openimmo-detail__headerleft > h1.openimmo-detail__title",
        "type": "text"
        },
        {
        "name": "address",
        "selector": "div.openimmo-detail__intro > div > p",
        "type": "text"
        },
        {
        "name": "price",
        "selector": "div.frame > div > div.row > section.openimmo-detail__rental-costs-container > ul > li:nth-child(3) > span.openimmo-detail__rental-costs-list-item-value",
        "type": "text"
        },
        {
        "name": "rooms",
        "selector": "div.openimmo-detail__object > ul.openimmo-detail__object-list > li:nth-of-type(1)",
        "type": "text"
        },
        {
        "name": "size",
        "selector": "div.openimmo-detail__object > ul.openimmo-detail__object-list > li:nth-of-type(2)",
        "type": "text"
        },
        {
        "name": "wbs_required",
        "selector": "div.openimmo-detail__object > ul.openimmo-detail__object-list > li:nth-of-type(6)",
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
                
                # Spezielle Bereinigung für WBS-Feld: extrahiere nur "Ja" oder "Nein"
                wbs_text = property_info.get('wbs_required', '').strip().lower()
                if wbs_text:
                    if 'ja' in wbs_text:
                        property_info['wbs_required'] = 'Ja'
                    elif 'nein' in wbs_text:
                        property_info['wbs_required'] = 'Nein'
                    else:
                        property_info['wbs_required'] = 'Nicht verfügbar'
                
                # Filter für 2-3 Zimmer
                rooms_text = property_info.get('rooms', '').strip()
                if rooms_text:
                    try:
                        # Extrahiere Zahl aus dem Text (z.B. "2 Zimmer" -> 2)
                        import re
                        rooms_match = re.search(r'([0-9,.]+)', rooms_text.replace(',', '.'))
                        if rooms_match:
                            rooms_number = float(rooms_match.group(1))
                            if 2 <= rooms_number <= 3:
                                all_properties.append(property_info)
                        else:
                            # Wenn keine Zahl gefunden wird, trotzdem hinzufügen
                            all_properties.append(property_info)
                    except (ValueError, AttributeError):
                        # Bei Fehlern trotzdem hinzufügen
                        all_properties.append(property_info)
                else:
                    # Wenn keine Zimmer-Info vorhanden ist, trotzdem hinzufügen
                    all_properties.append(property_info)
        else:
            print(f"Fehler bei {result.url}: {result.error_message}")
    
    return all_properties


async def crawl_list():
    css_strategy = JsonCssExtractionStrategy(schema={
        "baseSelector": "div.textWrap > div.btn-holder",
        "fields": [{"name": "link","selector": "a.immo-button-cta","type": "attribute","attribute": "href"}]
    })
    
    all_links = set()

    js_filter_interaction = """
    // Wait for page to load
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // 1. Select the filter option (5th child - anpassen falls nötig)
    const filterOption = document.querySelector('#openimmo-search-form > div.panel.panel-default.form-top > div > div:nth-child(4) > select > option:nth-child(5)');
    if (filterOption) {
        filterOption.selected = true;
        filterOption.parentElement.dispatchEvent(new Event('change', { bubbles: true }));
        await new Promise(resolve => setTimeout(resolve, 500));
    }
    
    // 2. Click the search submit button
    const searchSubmitButton = document.querySelector('#openimmo-search-form > div.panel.panel-default.form-top > div > div.submit-container > button');
    if (searchSubmitButton) {
        searchSubmitButton.click();
    }
    
    // Wait for search results to load
    await new Promise(resolve => setTimeout(resolve, 3000));
    """
    
    async with AsyncWebCrawler(config=BrowserConfig(headless=True)) as crawler:
        # Erste Seite
        result = await crawler.arun(
            url="https://www.wbm.de/wohnungen-berlin/angebote/",
            config=CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                extraction_strategy=css_strategy,
                js_code=js_filter_interaction,
                session_id="session",
                wait_for="css:article, .immo-col, .textWrap"
            )
        )
        
        if result.success:
            for prop in json.loads(result.extracted_content):
                all_links.add(prop.get('link'))

    all_urls = []
    
    for link in all_links:
        all_urls.append(f"https://www.wbm.de/{link}" if not link.startswith('http') else link)

    return all_urls

if __name__ == "__main__":
    asyncio.run(crawl())