class VonoviaExtractionSchema:
    SCHEMA_LISTING_URLS = {
        "baseSelector": "div.headlines > h2.h4.headline",
        "fields": [{"name": "link", "selector": "a", "type": "attribute", "attribute": "href"}]
    }
    SCHEMA_SINGLE_PROPERTY = {
    "name": "www.vonovia.de Schema",
    "baseSelector": "body",
    "fields": [
        {
        "name": "title",
        "selector": "body > div.template > div > div > div > div.estate-detail-page > div.real-estate-hero > div:nth-child(1) > div.content-card > div.content > div.headlines > h1",
        "type": "text"
        },
        {
        "name": "address",
        "selector": "body > div.template > div > div > div > div.estate-detail-page > div.real-estate-hero > div:nth-child(1) > div.wrapper > div > a > span",
        "type": "text"
        },
        {
        "name": "price",
        "selector": "body > div.template > div > div > div > div.estate-detail-page > div.container > main > div.side-left > div.real-estate-numbers > div:nth-child(2) > div > div > div > div",
        "type": "text"
        },
        {
        "name": "rooms",
        "selector": "body > div.template > div > div > div > div.estate-detail-page > div.container > main > div.side-left > div.real-estate-numbers > div:nth-child(5) > div > div > div > div",
        "type": "text"
        },
        {
        "name": "size",
        "selector": "body > div.template > div > div > div > div.estate-detail-page > div.container > main > div.side-left > div.real-estate-numbers > div:nth-child(3) > div > div > div > div",
        "type": "text"
        },
        {
        "name": "wbs_required",
        "selector": "N.A.",
        "type": "text"
        }
    ]
    }
    WAIT_FOR_ELEMENT = "body > div.template > div.main.container-fluid > div > div > div > div > div.list-api-based.list-real-estate.show > div > div.teaser-xl-container > div > div:nth-child(1) > div > div.image-slider > a"
    WAIT_FOR_LISTING_ELEMENT = "body > div.template > div > div > div > div.estate-detail-page > div.container > main > div.side-left > div.real-estate-numbers > div:nth-child(2) > div > div > div > div"