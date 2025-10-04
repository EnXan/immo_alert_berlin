// Wait for page to load
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // 1. First click on the element for rent including heating cost
        const element = document.querySelector('#openimmo-search-form > div:nth-child(5) > div:nth-child(1) > div > div:nth-child(1) > div > div > div > label > span.on');
        if (element) {
            element.click();
            await new Promise(resolve => setTimeout(resolve, 500));
        }
        
        // 2. Handle price dropdown
        const priceDropdown = document.querySelector('#uid-search-price-rental');
        if (priceDropdown) {
            priceDropdown.click();
            await new Promise(resolve => setTimeout(resolve, 500));

            // Helper function to determine price category
            function getPriceCategory(maxPrice) {
                if (maxPrice <= 300) return 300;
                if (maxPrice <= 400) return 400;
                if (maxPrice <= 500) return 500;
                if (maxPrice <= 700) return 700;
                if (maxPrice <= 900) return 900;
                if (maxPrice <= 1200) return 1200;
                return 'arbitrary';
            }

            switch (getPriceCategory(f.max_price)) {
                case 300:
                    const max300Option = document.querySelector('#form-multiselect-search-price-warm > div > fieldset:nth-child(1) > div > label:nth-child(2) > span.form-toggle__label');
                    max300Option.click();
                    break;
                case 400:
                    const max400Option = document.querySelector('#form-multiselect-search-price-warm > div > fieldset:nth-child(1) > div > label:nth-child(3) > span.form-toggle__label');
                    max400Option.click();
                    break;
                case 500:
                    const max500Option = document.querySelector('#form-multiselect-search-price-warm > div > fieldset:nth-child(1) > div > label:nth-child(4) > span.form-toggle__label');
                    max500Option.click();
                    break;
                case 700:
                    const max700Option = document.querySelector('#form-multiselect-search-price-warm > div > fieldset:nth-child(1) > div > label:nth-child(5) > span.form-toggle__label');
                    max700Option.click();
                    break;
                case 900:
                    const max900Option = document.querySelector('#form-multiselect-search-price-warm > div > fieldset:nth-child(1) > div > label:nth-child(6) > span.form-toggle__label');
                    max900Option.click();
                    break;
                case 1200:
                    const max1200Option = document.querySelector('#form-multiselect-search-price-warm > div > fieldset:nth-child(1) > div > label:nth-child(7) > span.form-toggle__label');
                    max1200Option.click();
                    break;
                default:
                    const arbitraryOption = document.querySelector('#form-multiselect-search-price-warm > div > fieldset:nth-child(1) > div > label:nth-child(1) > span.form-toggle__label');
                    arbitraryOption.click();
                    break;
            }

            /* Currently not working because of degewo website issues, will be activated later
            const vonInput = document.querySelector('input[name="tx_openimmo_immobilie[nettokaltmiete_start]"]');
            vonInput.value = f.min_price;

            const bisInput = document.querySelector('input[name="tx_openimmo_immobilie[nettokaltmiete_end]"]');
            bisInput.value = f.max_price;
            const confirm = document.querySelector('#form-multiselect-search-price-cold > div > fieldset.form-multiselect__custom > div > div.form-row__item.form-multiselect__custom-row-apply > button');
            if (confirm) {
                confirm.click();
            }
            */
        }
        
        await new Promise(resolve => setTimeout(resolve, 1000));

        // 3. Handle size selection
        // Helper function to determine size category based on min_size
        function getSizeCategory(minSize) {
            if (!minSize || minSize < 20) return 'beliebig';
            if (minSize >= 20 && minSize < 50) return 20;
            if (minSize >= 50 && minSize < 70) return 50;
            if (minSize >= 70 && minSize < 90) return 70;
            if (minSize >= 90 && minSize < 120) return 90;
            if (minSize >= 120) return 120;
            return 'beliebig';
        }

        const sizeCategory = getSizeCategory(f.min_size);
        let sizeSelector;

        switch (sizeCategory) {
            case 'beliebig':
                sizeSelector = '#openimmo-search-form > div:nth-child(5) > div:nth-child(2) > div > div > div > fieldset.form-group > div > label:nth-child(1) > input';
                break;
            case 20:
                sizeSelector = '#openimmo-search-form > div:nth-child(5) > div:nth-child(2) > div > div > div > fieldset.form-group > div > label:nth-child(2) > input';
                break;
            case 50:
                sizeSelector = '#openimmo-search-form > div:nth-child(5) > div:nth-child(2) > div > div > div > fieldset.form-group > div > label:nth-child(3) > input';
                break;
            case 70:
                sizeSelector = '#openimmo-search-form > div:nth-child(5) > div:nth-child(2) > div > div > div > fieldset.form-group > div > label:nth-child(4) > input';
                break;
            case 90:
                sizeSelector = '#openimmo-search-form > div:nth-child(5) > div:nth-child(2) > div > div > div > fieldset.form-group > div > label:nth-child(5) > input';
                break;
            case 120:
                sizeSelector = '#openimmo-search-form > div:nth-child(5) > div:nth-child(2) > div > div > div > fieldset.form-group > div > label:nth-child(6) > input';
                break;
        }

        if (sizeSelector) {
            const sizeOption = document.querySelector(sizeSelector);
            if (sizeOption && !sizeOption.checked) {
                sizeOption.click();
                await new Promise(resolve => setTimeout(resolve, 500));
            }
        }

        // 4. Handle WBS dropdown
        const wbsDropdown = document.querySelector('#uid-wbs');
        if (wbsDropdown) {
            wbsDropdown.click();
            await new Promise(resolve => setTimeout(resolve, 500));

            // Helper function to determine WBS category
            function getWbsCategory(wbsRequired) {
                if (wbsRequired === true) return 'ja';
                if (wbsRequired === false) return 'nein';
                return 'egal';
            }

            const wbsCategory = getWbsCategory(f.wbs_required);
            let wbsSelector;

            switch (wbsCategory) {
                case 'egal':
                    wbsSelector = '#openimmo-search-form > div:nth-child(6) > div:nth-child(3) > div > div > div > fieldset > div > label:nth-child(1) > input';
                    break;
                case 'ja':
                    wbsSelector = '#openimmo-search-form > div:nth-child(6) > div:nth-child(3) > div > div > div > fieldset > div > label:nth-child(2) > input';
                    break;
                case 'nein':
                    wbsSelector = '#openimmo-search-form > div:nth-child(6) > div:nth-child(3) > div > div > div > fieldset > div > label:nth-child(3) > input';
                    break;
            }

            if (wbsSelector) {
                const wbsOption = document.querySelector(wbsSelector);
                if (wbsOption && !wbsOption.checked) {
                    wbsOption.click();
                    await new Promise(resolve => setTimeout(resolve, 500));
                }
            }
        }
        
        // Wait for any form updates to process
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // 3. Click the search button
        const searchButton = document.querySelector('#openimmo-search-form > div:nth-child(8) > div > div:nth-child(1) > button.btn.btn--prim.btn--lg.btn--immosearch');
        if (searchButton) {
            searchButton.click();
        }
        
        // Wait for search results to load
        await new Promise(resolve => setTimeout(resolve, 2000));