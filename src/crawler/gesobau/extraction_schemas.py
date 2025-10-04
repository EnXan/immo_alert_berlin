class GesobauExtractionSchema:
    SCHEMA_LISTING_URLS = {
        "baseSelector": "h3.basicTeaser__title > span.basicTeaser__title__text",
        "fields": [{"name": "link","selector": "a","type": "attribute","attribute": "href"}]
    }
    SCHEMA_SINGLE_PROPERTY = {
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
    }
    NEXT_PAGE_SELECTOR_JS = "document.querySelector('#tx-solr-search > nav > ul > li:nth-child(2) > a')?.click()"
    WAIT_FOR_ELEMENT = "css:.basicTeaser__content, .teaserList, #tx-solr-search"
    WAIT_FOR_LISTING_ELEMENT = "#immoKosten > div > div > div:nth-child(1) > div:nth-child(1) > section > div > div.co__main > div > table > tbody > tr:nth-child(4) > td"