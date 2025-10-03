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
    LISTING_URLS_PRE_FILTER_JS = """
    // Wait for page to load
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // 1. Click on 2 rooms filter
    const roomsButton = document.querySelector('#rooms-2');
    if (roomsButton) {
        roomsButton.click();
        await new Promise(resolve => setTimeout(resolve, 500));
    }
    
    // 2. Click the search submit button
    const searchSubmitButton = document.querySelector('#flat-search-filter--form > div.container > div.filters > div > div.col-12.col-lg-2.col__submit.d-flex.align-items-end > button');
    if (searchSubmitButton) {
        searchSubmitButton.click();
    }
    
    // Wait for search results to load
    await new Promise(resolve => setTimeout(resolve, 3000));
    """