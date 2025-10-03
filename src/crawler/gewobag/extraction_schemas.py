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
    LISTING_URLS_PRE_FILTER_JS = """
    // Wait for page to load
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // 1. Click the rental options dialog button
    const dialogButton = document.querySelector('#rental-options-dialog-button');
    if (dialogButton) {
        dialogButton.click();
        await new Promise(resolve => setTimeout(resolve, 1000));
    }
    
    // 2. Fill max rent field with 900
    const maxRentInput = document.querySelector('#gesamtmiete_bis');
    if (maxRentInput) {
        maxRentInput.focus();
        maxRentInput.value = '900';
        maxRentInput.dispatchEvent(new Event('input', { bubbles: true }));
        maxRentInput.dispatchEvent(new Event('change', { bubbles: true }));
        await new Promise(resolve => setTimeout(resolve, 300));
    }
    
    // 3. Fill rooms from field with 2
    const roomsFromInput = document.querySelector('#zimmer_von');
    if (roomsFromInput) {
        roomsFromInput.focus();
        roomsFromInput.value = '2';
        roomsFromInput.dispatchEvent(new Event('input', { bubbles: true }));
        roomsFromInput.dispatchEvent(new Event('change', { bubbles: true }));
        await new Promise(resolve => setTimeout(resolve, 300));
    }
    
    // 4. Fill rooms to field with 3
    const roomsToInput = document.querySelector('#zimmer_bis');
    if (roomsToInput) {
        roomsToInput.focus();
        roomsToInput.value = '3';
        roomsToInput.dispatchEvent(new Event('input', { bubbles: true }));
        roomsToInput.dispatchEvent(new Event('change', { bubbles: true }));
        await new Promise(resolve => setTimeout(resolve, 300));
    }
    
    // 5. Click the search submit button
    const searchSubmitButton = document.querySelector('#search-submit');
    if (searchSubmitButton) {
        searchSubmitButton.click();
    }
    
    // Wait for search results to load
    await new Promise(resolve => setTimeout(resolve, 3000));
    """