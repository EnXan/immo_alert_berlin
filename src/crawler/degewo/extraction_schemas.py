class DegewoExtractionSchema:
    SCHEMA_LISTING_URLS = {
        "baseSelector": "article.article-list__item--immosearch",
        "fields": [{"name": "link", "selector": "a", "type": "attribute", "attribute": "href"}]
    }
    SCHEMA_SINGLE_PROPERTY = {
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
    }
    NEXT_PAGE_SELECTOR_JS = "document.querySelector('a.pager__next')?.click()"
    WAIT_FOR_ELEMENT = "css:article.article-list__item--immosearch"
    WAIT_FOR_LISTING_ELEMENT="body > div.frame.frame-default.frame-type-html.frame-layout-0.tx-openimmo.tx-openimmo-show > article > div > div > header > div.ce-table.expose__header-details > div > div:nth-child(3) > div"
    LISTING_URLS_PRE_FILTER_JS = """
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