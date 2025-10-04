// Wait for page to load
await new Promise(resolve => setTimeout(resolve, 2000));

// Click the rental options dialog button
const dialogButton = document.querySelector('#rental-options-dialog-button');
if (dialogButton) {
    dialogButton.click();
    await new Promise(resolve => setTimeout(resolve, 1000));
}

// Fill min_rent
const minRentInput = document.querySelector('#gesamtmiete_von');
if (minRentInput) {
    minRentInput.focus();
    minRentInput.value = f.min_price;
    minRentInput.dispatchEvent(new Event('input', { bubbles: true }));
    minRentInput.dispatchEvent(new Event('change', { bubbles: true }));
    await new Promise(resolve => setTimeout(resolve, 300));
}

// Fill max_rent
const maxRentInput = document.querySelector('#gesamtmiete_bis');
if (maxRentInput) {
    maxRentInput.focus();
    maxRentInput.value = f.max_price;
    maxRentInput.dispatchEvent(new Event('input', { bubbles: true }));
    maxRentInput.dispatchEvent(new Event('change', { bubbles: true }));
    await new Promise(resolve => setTimeout(resolve, 300));
}

// Fill min_size
const minSizeInput = document.querySelector('#gesamtflaeche_von');
if (minSizeInput) {
    minSizeInput.focus();
    minSizeInput.value = f.min_size;
    minSizeInput.dispatchEvent(new Event('input', { bubbles: true }));
    minSizeInput.dispatchEvent(new Event('change', { bubbles: true }));
    await new Promise(resolve => setTimeout(resolve, 300));
}

// Fill max_size
const maxSizeInput = document.querySelector('#gesamtflaeche_bis');
if (maxSizeInput) {
    maxSizeInput.focus();
    maxSizeInput.value = f.max_size;
    maxSizeInput.dispatchEvent(new Event('input', { bubbles: true }));
    maxSizeInput.dispatchEvent(new Event('change', { bubbles: true }));
    await new Promise(resolve => setTimeout(resolve, 300));
}

// Fill min_rooms
const roomsFromInput = document.querySelector('#zimmer_von');
if (roomsFromInput) {
    roomsFromInput.focus();
    roomsFromInput.value = f.min_rooms;
    roomsFromInput.dispatchEvent(new Event('input', { bubbles: true }));
    roomsFromInput.dispatchEvent(new Event('change', { bubbles: true }));
    await new Promise(resolve => setTimeout(resolve, 300));
}

// Fill max_rooms
const roomsToInput = document.querySelector('#zimmer_bis');
if (roomsToInput) {
    roomsToInput.focus();
    roomsToInput.value = f.max_rooms;
    roomsToInput.dispatchEvent(new Event('input', { bubbles: true }));
    roomsToInput.dispatchEvent(new Event('change', { bubbles: true }));
    await new Promise(resolve => setTimeout(resolve, 300));
}

// Handle WBS required checkbox
const wbsCheckbox = document.querySelector('#wbs');
if (wbsCheckbox && f.wbs_required === true) {
    // Only check if it's not already checked
    if (!wbsCheckbox.checked) {
        wbsCheckbox.focus();
        wbsCheckbox.click();
        wbsCheckbox.dispatchEvent(new Event('change', { bubbles: true }));
        await new Promise(resolve => setTimeout(resolve, 300));
    }
}

// Click the search submit button
const searchSubmitButton = document.querySelector('#search-submit');
if (searchSubmitButton) {
    searchSubmitButton.click();
}

// Wait for search results to load
await new Promise(resolve => setTimeout(resolve, 3000));