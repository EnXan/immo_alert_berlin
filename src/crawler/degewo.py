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
    "name": "www.degewo.de Schema",
    "baseSelector": "body",
    "fields": [
        {
        "name": "title",
        "selector": "body > div.frame.frame-default.frame-type-html.frame-layout-0.tx-openimmo.tx-openimmo-show > article > div > div > header > h1",
        "type": "text"
        },
        {
        "name": "address",
        "selector": "body > div.frame.frame-default.frame-type-html.frame-layout-0.tx-openimmo.tx-openimmo-show > article > div > div > header > span.expose__meta",
        "type": "text"
        },
        {
        "name": "price",
        "selector": "body > div.frame.frame-default.frame-type-html.frame-layout-0.tx-openimmo.tx-openimmo-show > article > div > div > header > div.ce-table.expose__header-details > div > div:nth-child(3) > div",
        "type": "text"
        },
        {
        "name": "rooms",
        "selector": "body > div.frame.frame-default.frame-type-html.frame-layout-0.tx-openimmo.tx-openimmo-show > div.section.section--md > section:nth-child(1) > div.teaser-tileset__col-1 > section > div > table > tbody > tr:nth-child(1) > td:nth-child(2)",
        "type": "text"
        },
        {
        "name": "size",
        "selector": "body > div.frame.frame-default.frame-type-html.frame-layout-0.tx-openimmo.tx-openimmo-show > div.section.section--md > section:nth-child(1) > div.teaser-tileset__col-1 > section > div > table > tbody > tr:nth-child(2) > td:nth-child(2)",
        "type": "text"
        },
        {
        "name": "wbs_required",
        "selector": "body > div.frame.frame-default.frame-type-html.frame-layout-0.tx-openimmo.tx-openimmo-show > div.section.section--md > section:nth-child(1) > div.teaser-tileset__col-1 > section > div > table > tbody > tr:nth-child(7) > td:nth-child(2)",
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
                
                # Filter für 2-3 Zimmer
                rooms_text = property_info.get('rooms', '').strip()
                if rooms_text:
                    try:
                        # Extrahiere Zahl aus dem Text (z.B. "2 Zimmer" -> 2)
                        rooms_number = float(rooms_text.split()[0].replace(',', '.'))
                        if 2 <= rooms_number <= 3:
                            all_properties.append(property_info)
                    except (ValueError, IndexError):
                        # Wenn keine gültige Zahl gefunden wird, trotzdem hinzufügen
                        all_properties.append(property_info)
                else:
                    # Wenn keine Zimmer-Info vorhanden ist, trotzdem hinzufügen
                    all_properties.append(property_info)
        else:
            print(f"Fehler bei {result.url}: {result.error_message}")
    
    return all_properties


async def crawl_list():
    css_strategy = JsonCssExtractionStrategy(schema={
        "baseSelector": "article.article-list__item--immosearch",
        "fields": [{"name": "link", "selector": "a", "type": "attribute", "attribute": "href"}]
    })
    
    all_links = set()

    js_filter_interaction = """
    // Wait for page to load
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // 1. First click on the preliminary element
    const preliminaryElement = document.querySelector('#openimmo-search-form > div:nth-child(5) > div:nth-child(1) > div > div:nth-child(1) > div > div > div > label > span.on');
    if (preliminaryElement) {
        preliminaryElement.click();
        await new Promise(resolve => setTimeout(resolve, 500));
    }
    
    // 2. Handle price dropdown
    const priceDropdown = document.querySelector('#uid-search-price-rental');
    if (priceDropdown) {
        priceDropdown.click();
        await new Promise(resolve => setTimeout(resolve, 500));
        
        const priceOption = document.querySelector('#form-multiselect-search-price-warm > div > fieldset:nth-child(1) > div > label:nth-child(6) > span.form-toggle__label');
        if (priceOption) {
            priceOption.click();
        }
    }
    
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Wait for any form updates to process
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 3. Click the search button
    const searchButton = document.querySelector('#openimmo-search-form > div:nth-child(8) > div > div:nth-child(1) > button.btn.btn--prim.btn--lg.btn--immosearch');
    if (searchButton) {
        searchButton.click();
    }
    
    // Wait for search results to load
    await new Promise(resolve => setTimeout(resolve, 2000));
    """
    
    async with AsyncWebCrawler(config=BrowserConfig(headless=True)) as crawler:
        # Erste Seite
        result = await crawler.arun(
            url="https://www.degewo.de/immosuche/",
            config=CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                extraction_strategy=css_strategy,
                js_code=js_filter_interaction,
                session_id="session",
                wait_for="css:article.article-list__item--immosearch"
            )
        )
        
        if result.success:
            for prop in json.loads(result.extracted_content):
                all_links.add(prop.get('link'))
        
        # Weitere Seiten
        for page in range(2, 11):
            result = await crawler.arun(
                url="https://www.degewo.de/immosuche/",
                config=CrawlerRunConfig(
                    cache_mode=CacheMode.BYPASS,
                    extraction_strategy=css_strategy,
                    session_id="session",
                    js_code="document.querySelector('a.pager__next')?.click()",
                    js_only=True,
                    wait_for="css:article.article-list__item--immosearch",
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
        all_urls.append(f"https://www.degewo.de{link}" if not link.startswith('http') else link)

    return all_urls

if __name__ == "__main__":
    asyncio.run(crawl())