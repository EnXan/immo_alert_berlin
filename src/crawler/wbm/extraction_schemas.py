class WBMExtractionSchema:
    SCHEMA_LISTING_URLS = {
        "baseSelector": "div.textWrap > div.btn-holder",
        "fields": [{"name": "link","selector": "a.immo-button-cta","type": "attribute","attribute": "href"}]
    }
    SCHEMA_SINGLE_PROPERTY = {
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
    }
    WAIT_FOR_ELEMENT = "css:article, .immo-col, .textWrap"
    WAIT_FOR_LISTING_ELEMENT = "#c105 > div > div.row > section.openimmo-detail__rental-costs-container > ul > li:nth-child(3) > span.openimmo-detail__rental-costs-list-item-value"