class GewobagExtractionSchema:
    SCHEMA_LISTING_URLS = {
        "baseSelector": "article.angebot-big-box > div.angebot-content > div.angebot-footer",
        "fields": [{"name": "link","selector": "a.read-more-link","type": "attribute","attribute": "href"}]
    }
    SCHEMA_SINGLE_PROPERTY = {
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
    }
    WAIT_FOR_ELEMENT = "css:article.angebot-big-box"
    WAIT_FOR_LISTING_ELEMENT = "#rental-overview > div.overview-details > table.overview-table.details-price > tbody > tr.interest > td"