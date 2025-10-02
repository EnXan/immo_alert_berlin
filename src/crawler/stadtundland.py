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
    "name": "stadtundland.de Schema",
    "baseSelector": "body",
    "fields": [
        {
        "name": "title",
        "selector": "#printArea > h1",
        "type": "text"
        },
        {
        "name": "address",
        "selector": "#printArea > p.introText.ImmoDetail_address__ZGae3",
        "type": "text"
        },
        {
        "name": "price",
        "selector": "#printArea > div.ImmoDetail_tableWrapper__6mtVl > div > table > tbody > tr > th:-soup-contains('Gesamtmiete') + td",
        "type": "text"
        },
        {
        "name": "rooms",
        "selector": "#printArea > div.ImmoDetail_tableWrapper__6mtVl > div > table > tbody > tr:nth-child(6) > td",
        "type": "text"
        },
        {
        "name": "size",
        "selector": "#printArea > div.ImmoDetail_tableWrapper__6mtVl > div > table > tbody > tr:nth-child(5) > td",
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
    
    for i, result in enumerate(results):
        
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
                
                # Filter für Warmmiete < 900€
                price_text = property_info.get('price', '').strip()
                
                if price_text:
                    try:
                        # Extrahiere Zahl aus dem Text und handle deutsche Zahlenformate
                        import re
                        # Entferne Euro-Symbol und Whitespace
                        clean_price = price_text.replace('€', '').strip()
                        
                        # Handle deutsche Zahlenformate: 1.234,56 oder 1234,56 oder 1234.56
                        # Wenn es einen Punkt vor dem Komma gibt, ist es Tausendertrennzeichen
                        if '.' in clean_price and ',' in clean_price:
                            # Format: 1.234,56 -> 1234.56
                            clean_price = clean_price.replace('.', '').replace(',', '.')
                        elif ',' in clean_price and clean_price.count(',') == 1:
                            # Format: 1234,56 -> 1234.56
                            clean_price = clean_price.replace(',', '.')
                        # Sonst bleibt es wie es ist (1234.56)
                        
                        price_match = re.search(r'([0-9.]+)', clean_price)
                        
                        if price_match:
                            price_number = float(price_match.group(1))
                            
                            if price_number < 900:
                                all_properties.append(property_info)
                        else:
                            # Wenn keine Zahl gefunden wird, trotzdem hinzufügen
                            all_properties.append(property_info)
                    except (ValueError, AttributeError) as e:
                        # Bei Fehlern trotzdem hinzufügen
                        all_properties.append(property_info)
                else:
                    # Wenn keine Preis-Info vorhanden ist, trotzdem hinzufügen
                    all_properties.append(property_info)
    
    return all_properties


async def crawl_list():
    all_links = set()

    js_filter_interaction = """
    // Wait for page to load
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // 1. Fill minimum rooms field with 2
    const minRoomsInput = document.querySelector('#appartment-search > form > div.ApartmentSearch_formSection__THrPC > div.ApartmentSearch_formGroup__KhnHp.ApartmentSearch_areaGroup__WR8f8 > div.ApartmentSearch_inputContainer___o7oW > div.ApartmentSearch_formRow__kLeoE.ApartmentSearch_areaRow__RdbZk > div:nth-child(1) > div > input[type=text]');
    if (minRoomsInput) {
        minRoomsInput.focus();
        minRoomsInput.value = '2';
        minRoomsInput.dispatchEvent(new Event('input', { bubbles: true }));
        minRoomsInput.dispatchEvent(new Event('change', { bubbles: true }));
        await new Promise(resolve => setTimeout(resolve, 500));
    }
    
    // 2. Fill maximum rooms field with 3
    const maxRoomsInput = document.querySelector('#appartment-search > form > div.ApartmentSearch_formSection__THrPC > div.ApartmentSearch_formGroup__KhnHp.ApartmentSearch_areaGroup__WR8f8 > div.ApartmentSearch_inputContainer___o7oW > div.ApartmentSearch_formRow__kLeoE.ApartmentSearch_areaRow__RdbZk > div:nth-child(2) > div > input[type=text]');
    if (maxRoomsInput) {
        maxRoomsInput.focus();
        maxRoomsInput.value = '3';
        maxRoomsInput.dispatchEvent(new Event('input', { bubbles: true }));
        maxRoomsInput.dispatchEvent(new Event('change', { bubbles: true }));
        await new Promise(resolve => setTimeout(resolve, 500));
    }
    
    // Wait for form updates to process
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 3. Click the search button
    const searchButton = document.querySelector('#appartment-search > form > div.ApartmentSearch_formSection__THrPC > div.ApartmentSearch_formGroup__KhnHp.ApartmentSearch_areaGroup__WR8f8 > button');
    if (searchButton) {
        searchButton.click();
    }
    
    // Wait for search results to load
    await new Promise(resolve => setTimeout(resolve, 3000));
    """
    
    async with AsyncWebCrawler(config=BrowserConfig(headless=True)) as crawler:
        # Erste Seite
        result = await crawler.arun(
            url="https://stadtundland.de/wohnungssuche/",
            config=CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                js_code=js_filter_interaction,
                session_id="session",
                wait_for="css:.ImmoSearchResults_results, .Teaser_immoTeaser__content, article"
            )
        )
        
        if result.success:
            # Extract links from markdown content using regex
            import re
            markdown_content = result.markdown
            
            # Find all links that contain /wohnungssuche/ pattern
            link_pattern = r'https://stadtundland\.de/wohnungssuche/[^\s\)]+(?=%2F|\)|\s|$)'
            found_links = re.findall(link_pattern, markdown_content)
            
            for link in found_links:
                # Clean up the link (remove URL encoding if needed)
                clean_link = link.replace('%2F', '/')
                all_links.add(clean_link)
        
        # Weitere Ergebnisse laden durch "Load More" Button
        for load_attempt in range(1, 20): 
            result = await crawler.arun(
                url="https://stadtundland.de/wohnungssuche/",
                config=CrawlerRunConfig(
                    cache_mode=CacheMode.BYPASS,
                    session_id="session",
                    js_code="""
                    // Klick auf "Mehr Ergebnisse laden" Button
                    const loadMoreBtn = document.querySelector('#main > div > div.ImmoSearchResults_results__sMV01 > div.ImmoSearchResults_pagination-button-container__RAxkf > button');
                    if (loadMoreBtn && !loadMoreBtn.disabled && loadMoreBtn.style.display !== 'none') {
                        loadMoreBtn.click();
                        // Warten bis neue Ergebnisse geladen sind
                        await new Promise(resolve => setTimeout(resolve, 3000));
                    } else {
                        // Kein Button gefunden oder disabled - beenden
                        throw new Error('No more results to load');
                    }
                    """,
                    js_only=True,
                    wait_for="css:.ImmoSearchResults_results, .Teaser_immoTeaser__content, article",
                )
            )
            
            if not result.success:
                break
                
            # Extract links from markdown content using regex for load more attempts too
            import re
            markdown_content = result.markdown
            
            # Find all links that contain /wohnungssuche/ pattern
            link_pattern = r'https://stadtundland\.de/wohnungssuche/[^\s\)]+(?=%2F|\)|\s|$)'
            found_links = re.findall(link_pattern, markdown_content)
            
            new_links = set()
            for link in found_links:
                # Clean up the link (remove URL encoding if needed)
                clean_link = link.replace('%2F', '/')
                new_links.add(clean_link)
            
            if not new_links or new_links.issubset(all_links):
                break
            all_links.update(new_links)

    all_urls = []
    
    for link in all_links:
        full_url = f"https://stadtundland.de{link}" if not link.startswith('http') else link
        all_urls.append(full_url)

    return all_urls

if __name__ == "__main__":
    asyncio.run(crawl())