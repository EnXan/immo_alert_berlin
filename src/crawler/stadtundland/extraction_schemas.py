class StadtUndLandExtractionSchema:
    SCHEMA_SINGLE_PROPERTY = {
    "name": "stadtundland.de Schema",
    "baseSelector": "body",
    "fields": [
        {
        "name": "title",
        "selector": "#printArea > h1",
        "type": "text"
        },
        {
        "name": "address",
        "selector": "#printArea > p.introText.ImmoDetail_address__ZGae3",
        "type": "text"
        },
        {
        "name": "price",
        "selector": "#printArea > div.ImmoDetail_tableWrapper__6mtVl > div > table > tbody > tr > th:-soup-contains('Gesamtmiete') + td",
        "type": "text"
        },
        {
        "name": "rooms",
        "selector": "#printArea > div.ImmoDetail_tableWrapper__6mtVl > div > table > tbody > tr:nth-child(6) > td",
        "type": "text"
        },
        {
        "name": "size",
        "selector": "#printArea > div.ImmoDetail_tableWrapper__6mtVl > div > table > tbody > tr:nth-child(5) > td",
        "type": "text"
        },
        {
        "name": "wbs_required",
        "selector": "N.A.",
        "type": "text"
        }
    ]
    }
    LISTING_URLS_PRE_FILTER_JS = """
    // Wait for page to load
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // 1. Fill minimum rooms field with 2
    const minRoomsInput = document.querySelector('#appartment-search > form > div.ApartmentSearch_formSection__THrPC > div.ApartmentSearch_formGroup__KhnHp.ApartmentSearch_areaGroup__WR8f8 > div.ApartmentSearch_inputContainer___o7oW > div.ApartmentSearch_formRow__kLeoE.ApartmentSearch_areaRow__RdbZk > div:nth-child(1) > div > input[type=text]');
    if (minRoomsInput) {
        minRoomsInput.focus();
        minRoomsInput.value = '2';
        minRoomsInput.dispatchEvent(new Event('input', { bubbles: true }));
        minRoomsInput.dispatchEvent(new Event('change', { bubbles: true }));
        await new Promise(resolve => setTimeout(resolve, 500));
    }
    
    // 2. Fill maximum rooms field with 3
    const maxRoomsInput = document.querySelector('#appartment-search > form > div.ApartmentSearch_formSection__THrPC > div.ApartmentSearch_formGroup__KhnHp.ApartmentSearch_areaGroup__WR8f8 > div.ApartmentSearch_inputContainer___o7oW > div.ApartmentSearch_formRow__kLeoE.ApartmentSearch_areaRow__RdbZk > div:nth-child(2) > div > input[type=text]');
    if (maxRoomsInput) {
        maxRoomsInput.focus();
        maxRoomsInput.value = '3';
        maxRoomsInput.dispatchEvent(new Event('input', { bubbles: true }));
        maxRoomsInput.dispatchEvent(new Event('change', { bubbles: true }));
        await new Promise(resolve => setTimeout(resolve, 500));
    }
    
    // Wait for form updates to process
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 3. Click the search button
    const searchButton = document.querySelector('#appartment-search > form > div.ApartmentSearch_formSection__THrPC > div.ApartmentSearch_formGroup__KhnHp.ApartmentSearch_areaGroup__WR8f8 > button');
    if (searchButton) {
        searchButton.click();
    }
    
    // Wait for search results to load
    await new Promise(resolve => setTimeout(resolve, 3000));
    """
    LOAD_MORE_JS = """
    // Klick auf "Mehr Ergebnisse laden" Button
    const loadMoreBtn = document.querySelector('#main > div > div.ImmoSearchResults_results__sMV01 > div.ImmoSearchResults_pagination-button-container__RAxkf > button');
    if (loadMoreBtn && !loadMoreBtn.disabled && loadMoreBtn.style.display !== 'none') {
        loadMoreBtn.click();
        // Warten bis neue Ergebnisse geladen sind
        await new Promise(resolve => setTimeout(resolve, 3000));
    } else {
        // Kein Button gefunden oder disabled - beenden
        throw new Error('No more results to load');
    }
    """
    WAIT_FOR = "css:.ImmoSearchResults_results, .Teaser_immoTeaser__content, article"
    WAIT_FOR_LISTING_ELEMENT = "#printArea > div.ImmoDetail_tableWrapper__6mtVl > div > table > tbody > tr:nth-child(11) > td"