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