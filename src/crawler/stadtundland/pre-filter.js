// Helper function for React inputs
function setReactValue(element, value) {
    const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
        window.HTMLInputElement.prototype,
        'value'
    ).set;
    nativeInputValueSetter.call(element, value);
    
    element.dispatchEvent(new Event('input', { bubbles: true }));
    element.dispatchEvent(new Event('change', { bubbles: true }));
    element.dispatchEvent(new Event('blur', { bubbles: true }));
}

// Wait for page to load
await new Promise(resolve => setTimeout(resolve, 2000));
console.log("Page loaded");

// Fill minimum rooms
const minRoomsInput = document.querySelector('#appartment-search > form > div.ApartmentSearch_formSection__THrPC > div.ApartmentSearch_formGroup__KhnHp.ApartmentSearch_areaGroup__WR8f8 > div.ApartmentSearch_inputContainer___o7oW > div.ApartmentSearch_formRow__kLeoE.ApartmentSearch_areaRow__RdbZk > div:nth-child(1) > div > input[type=text]');
console.log(minRoomsInput);
if (minRoomsInput) {
    minRoomsInput.focus();
    if (f.min_rooms) {
        setReactValue(minRoomsInput, f.min_rooms.toString());
    }
    minRoomsInput.blur();
    await new Promise(resolve => setTimeout(resolve, 500));
}

// Fill maximum rooms
const maxRoomsInput = document.querySelector('#appartment-search > form > div.ApartmentSearch_formSection__THrPC > div.ApartmentSearch_formGroup__KhnHp.ApartmentSearch_areaGroup__WR8f8 > div.ApartmentSearch_inputContainer___o7oW > div.ApartmentSearch_formRow__kLeoE.ApartmentSearch_areaRow__RdbZk > div:nth-child(2) > div > input[type=text]');
console.log(maxRoomsInput);
if (maxRoomsInput) {
    maxRoomsInput.focus();
    if (f.max_rooms) {
        setReactValue(maxRoomsInput, f.max_rooms.toString());
    }
    maxRoomsInput.blur();
    await new Promise(resolve => setTimeout(resolve, 500));
}

const searchButtonOne = document.querySelector('#appartment-search > form > div.ApartmentSearch_formSection__THrPC > div.ApartmentSearch_formGroup__KhnHp.ApartmentSearch_areaGroup__WR8f8 > button');
if (searchButtonOne) {
    console.log("Clicking search button");
    searchButtonOne.click();
}

await new Promise(resolve => setTimeout(resolve, 1000));

// Fill minimum rent
const minRentInput = document.querySelector('#main > div > div.ImmoFilter_desktopFilters__JLawd > form > div:nth-child(3) > div.ImmoFilter_innerInputs__uqGiP > div:nth-child(1) > div > input[type=number]');
console.log(minRentInput);
if (minRentInput) {
    minRentInput.focus();
    if (f.min_price) {
        setReactValue(minRentInput, f.min_price);
    }
    minRentInput.blur();
    await new Promise(resolve => setTimeout(resolve, 500));
}

// Fill maximum rent
const maxRentInput = document.querySelector('#main > div > div.ImmoFilter_desktopFilters__JLawd > form > div:nth-child(3) > div.ImmoFilter_innerInputs__uqGiP > div:nth-child(2) > div > input[type=number]');
console.log(maxRentInput);
if (maxRentInput) {
    maxRentInput.focus();
    if (f.max_price) {
        setReactValue(maxRentInput, f.max_price);
    }
    maxRentInput.blur();
    await new Promise(resolve => setTimeout(resolve, 500));
}

// Fill minimum size
const minSizeInput = document.querySelector('#main > div > div.ImmoFilter_desktopFilters__JLawd > form > div:nth-child(4) > div.ImmoFilter_innerInputs__uqGiP > div:nth-child(1) > div > input[type=number]');
if (minSizeInput) {
    minSizeInput.focus();
    if (f.min_size) {
        setReactValue(minSizeInput, f.min_size);
    }
    minSizeInput.blur();
    await new Promise(resolve => setTimeout(resolve, 500));
}

// Fill maximum size
const maxSizeInput = document.querySelector('#main > div > div.ImmoFilter_desktopFilters__JLawd > form > div:nth-child(4) > div.ImmoFilter_innerInputs__uqGiP > div:nth-child(2) > div > input[type=number]');
if (maxSizeInput) {
    maxSizeInput.focus();
    if (f.max_size) {
        setReactValue(maxSizeInput, f.max_size);
    }
    maxSizeInput.blur();
    await new Promise(resolve => setTimeout(resolve, 500));
}

// Handle WBS required checkbox
const wbsCheckbox = document.querySelector('#main > div > div.ImmoFilter_desktopFilters__JLawd > form > div.ImmoFilter_checkboxGroup__TY4IK > div > div:nth-child(3) > div > input[type=checkbox]');
if (wbsCheckbox && f.wbs_required === true) {
    // Only check if it's not already checked
    if (!wbsCheckbox.checked) {
        wbsCheckbox.focus();
        wbsCheckbox.click();
        wbsCheckbox.dispatchEvent(new Event('change', { bubbles: true }));
        await new Promise(resolve => setTimeout(resolve, 500));
    }
}


const searchButtonTwo = document.querySelector('#main > div > div.ImmoFilter_desktopFilters__JLawd > form > div.ImmoFilter_fillterButtonContainer__JARig > button.Button_button__JnZ4E.Button_button__primary__FME8s');
if (searchButtonTwo) {
    searchButtonTwo.click();
}

// Wait for form updates
await new Promise(resolve => setTimeout(resolve,500));