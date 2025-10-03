from database.models import Property

def normalize_property(data):
    """Normalize property data to ensure consistency."""
    # Create Property object from input data (assuming data is a dict)
    if isinstance(data, dict):
        # Convert string values to proper types before creating Property object
        price = _normalize_price(data.get('price', ''))
        size = _normalize_size(data.get('size', ''))
        
        # Handle rooms conversion
        rooms_str = data.get('rooms', '')
        try:
            rooms = float(rooms_str) if rooms_str else 0.0
        except (ValueError, TypeError):
            rooms = 0.0
        
        # Handle wbs_required conversion
        wbs_raw = data.get('wbs_required', None)
        if isinstance(wbs_raw, str):
            wbs_required = wbs_raw.lower() in ['benötigt', '1', 'ja', 'yes', 'true', 'nein']
        else:
            wbs_required = False
        
        property = Property(
            title=data.get('title', 'No Title'),
            address=data.get('address', ''),
            price=price,
            rooms=rooms,
            size=size,
            wbs_required=wbs_required,
            source=data.get('source', 'unknown'),
            url=data.get('url', None)
        )
    else:
        property = data  # Assume it's already a Property object
    
    # Basisnormalisierung (string trimming)
    property = _base_normalize(property)
    
    # Weitere spezifische Normalisierungen
    property.address = _normalize_address(property.address)

    return property


def _base_normalize(data: Property):
    """Basic normalization steps applicable to all properties."""
    for field in data.__dataclass_fields__:
        value = getattr(data, field)
        if isinstance(value, str):
            normalized_value = value.strip()
            setattr(data, field, normalized_value)
    
    return data

def _normalize_address(address: str) -> str:
    """Ensure address is a clean string."""
    if not address:
        return ""
    return ' '.join(address.split())

def _normalize_price(price: str) -> float:
    """Ensure price has no strange characters and is a valid float."""
    if not price:
        return 0.0
    cleaned_price = ''.join(c for c in price if c.isdigit() or c in {'.', ','})
    cleaned_price = cleaned_price.replace(',', '.')
    try:
        return float(cleaned_price)
    except ValueError:
        return 0.0
    
def _normalize_size(size: str) -> float:
    """Ensure size has no strange characters and is a valid float."""
    if not size:
        return 0.0
    cleaned_size = ''.join(c for c in size if c.isdigit() or c in {'.', ','})
    cleaned_size = cleaned_size.replace(',', '.')
    try:
        return float(cleaned_size)
    except ValueError:
        return 0.0