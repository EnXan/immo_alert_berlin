// Wait for page to load
await new Promise(resolve => setTimeout(resolve, 2000));

// 1. Click on rooms filter
let roomsButton;
switch (f.min_rooms) {
    case 2:
        roomsButton = document.querySelector('#rooms-2');
        break;
    case 3:
        roomsButton = document.querySelector('#rooms-3');
        break;
    case 4:
        roomsButton = document.querySelector('#rooms-4');
        break;
    default:
        roomsButton = document.querySelector('#rooms-all');
        break;
}
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