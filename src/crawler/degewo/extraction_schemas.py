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