// Wait for page to load
await new Promise(resolve => setTimeout(resolve, 2000));

// 1. Fill rooms field
const roomsInput = document.querySelector('#facetzimmer-input');
if (roomsInput) {
    roomsInput.focus();
    console.log(f);
    roomsInput.value = f.min_rooms;
    roomsInput.dispatchEvent(new Event('input', { bubbles: true }));
    roomsInput.dispatchEvent(new Event('change', { bubbles: true }));
    await new Promise(resolve => setTimeout(resolve, 500));
}

// 2. Fill warm rent field
const warmRentInput = document.querySelector('#facetwarmmiete-input');
if (warmRentInput) {
    warmRentInput.focus();
    warmRentInput.value = f.max_price;
    warmRentInput.dispatchEvent(new Event('input', { bubbles: true }));
    warmRentInput.dispatchEvent(new Event('change', { bubbles: true }));
    await new Promise(resolve => setTimeout(resolve, 500));
}

// 3. Fill min size
const minSizeInput = document.querySelector('#facetwohnflaeche-input');
if (minSizeInput) {
    minSizeInput.focus();
    minSizeInput.value = f.min_size;
    minSizeInput.dispatchEvent(new Event('input', { bubbles: true }));
    minSizeInput.dispatchEvent(new Event('change', { bubbles: true }));
    await new Promise(resolve => setTimeout(resolve, 500));
}

// Wait for form updates to process
await new Promise(resolve => setTimeout(resolve, 1000));

// 3. Click the submit button
const submitButton = document.querySelector('#submit-facets');
if (submitButton) {
    submitButton.click();
}

// Wait for search results to load
await new Promise(resolve => setTimeout(resolve, 2000));

