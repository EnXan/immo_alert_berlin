from database.models import Property
import re

def normalize_property(data):
    """Normalize property data to ensure consistency."""
    if isinstance(data, dict):
        # Remove old postal_codes field if present to avoid conflicts
        data_copy = data.copy()
        data_copy.pop('postal_codes', None)
        
        # Normalize each field
        price = _normalize_price(data_copy.get('price', ''))
        size = _normalize_size(data_copy.get('size', ''))
        rooms = _normalize_rooms(data_copy.get('rooms', ''))
        wbs_required = _normalize_wbs(data_copy.get('wbs_required', ''))
        
        postal_code = _extract_postal_code(data_copy.get('address', ''))
        
        property = Property(
            title=data_copy.get('title', 'No Title').strip(),
            address=_normalize_address(data_copy.get('address', '')),
            price=price,
            rooms=rooms,
            size=size,
            wbs_required=wbs_required,
            postal_code=postal_code,
            source=data_copy.get('source', 'unknown'),
            url=data_copy.get('url', None)
        )
    else:
        property = data
    
    return property


def _normalize_address(address: str) -> str:
    """Clean address string."""
    if not address:
        return ""
    # Remove "Adresse:" prefix (from Howoge)
    address = address.replace('Adresse:', '').strip()
    # Clean whitespace
    address = ' '.join(address.split())
    # Replace pipe with comma
    address = address.replace(' | ', ', ')
    return address


def _normalize_price(price: str) -> float:
    """Extract price from various formats."""
    if not price:
        return 0.0
    
    # Remove common text
    price = price.replace('EUR', '').replace('€', '').replace('Euro', '')
    price = price.replace('Gesamt', '').replace('\xa0', ' ')
    
    # Remove all whitespace
    price = ''.join(price.split())
    
    # Handle German number format: 1.234,56 -> 1234.56
    # If both . and , exist, . is thousand separator
    if '.' in price and ',' in price:
        price = price.replace('.', '').replace(',', '.')
    # If only comma, it's decimal separator
    elif ',' in price:
        price = price.replace(',', '.')
    
    # Extract first number found
    match = re.search(r'(\d+\.?\d*)', price)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return 0.0
    
    return 0.0


def _normalize_size(size: str) -> float:
    """Extract size from various formats."""
    if not size:
        return 0.0
    
    # Remove common text
    size = size.replace('m²', '').replace('m2', '').replace('qm', '')
    size = size.replace('Größe:', '').replace('ca.', '').replace('\xa0', ' ')
    
    # Remove all whitespace
    size = ''.join(size.split())
    
    # Handle German number format
    if '.' in size and ',' in size:
        size = size.replace('.', '').replace(',', '.')
    elif ',' in size:
        size = size.replace(',', '.')
    
    # Extract first number found
    match = re.search(r'(\d+\.?\d*)', size)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return 0.0
    
    return 0.0


def _normalize_rooms(rooms: str) -> float:
    """Extract room count from various formats."""
    if not rooms:
        return 0.0
    
    # Remove common text
    rooms = rooms.replace('Anzahl der Zimmer:', '').replace('Zimmer:', '')
    rooms = rooms.strip()
    
    # Handle comma as decimal separator
    rooms = rooms.replace(',', '.')
    
    # Extract first number found
    match = re.search(r'(\d+\.?\d*)', rooms)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return 0.0
    
    return 0.0


def _normalize_wbs(wbs: str) -> bool:
    """Extract WBS requirement."""
    if not wbs or wbs == 'N.A.':
        return False
    
    wbs_lower = wbs.lower()
    
    # Remove prefix
    wbs_lower = wbs_lower.replace('wbs erforderlich:', '').strip()
    
    # Check for positive indicators
    if any(word in wbs_lower for word in ['ja', 'yes', 'true', 'benötigt', 'erforderlich']):
        return True
    
    # Check for negative indicators
    if any(word in wbs_lower for word in ['nein', 'no', 'false', 'nicht']):
        return False
    
    return False


def _extract_postal_code(address: str) -> str:
    """Extract postal code from address string."""
    if not address:
        return ""
    
    # Find first 5-digit postal code (German format)
    match = re.search(r'\b\d{5}\b', address)
    if match:
        return match.group(0)
    return ""