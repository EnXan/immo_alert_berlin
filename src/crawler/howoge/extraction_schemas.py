class HowogeExtractionSchema:
    SCHEMA_LISTING_URLS = {
        "baseSelector": "div.content > div.address",
        "fields": [{"name": "link","selector": "a.flat-single--link","type": "attribute","attribute": "href"}]
    }
    SCHEMA_SINGLE_PROPERTY = {
    "name": "www.howoge.de Schema",
    "baseSelector": "body",
    "fields": [
        {
        "name": "title",
        "selector": "#main > div.ce-wrapper.flat-detail__stage.background-color-petrol-brighter > div > div.data > h1",
        "type": "text"
        },
        {
        "name": "address",
        "selector": "#main > div.ce-wrapper.flat-detail__stage.background-color-petrol-brighter > div > div.data > div > p",
        "type": "text"
        },
        {
        "name": "price",
        "selector": "#main > div.ce-wrapper.flat-detail__stage.background-color-petrol-brighter > div > div.data > dl > div:nth-child(1) > dd",
        "type": "text"
        },
        {
        "name": "rooms",
        "selector": "#main > div.ce-wrapper.flat-detail__stage.background-color-petrol-brighter > div > div.data > dl > div:nth-child(3) > dd",
        "type": "text"
        },
        {
        "name": "size",
        "selector": "#main > div.ce-wrapper.flat-detail__stage.background-color-petrol-brighter > div > div.data > dl > div:nth-child(2) > dd",
        "type": "text"
        },
        {
        "name": "wbs_required",
        "selector": "N.A.",
        "type": "text"
        }
    ]
    }
    WAIT_FOR_ELEMENT = "#immoobject-list-2 > div"
    WAIT_FOR_LISTING_ELEMENT = "#main > div.ce-wrapper.flat-detail__stage.background-color-petrol-brighter > div > div.data > dl > div:nth-child(1) > dd"