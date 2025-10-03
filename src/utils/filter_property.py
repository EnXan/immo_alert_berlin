from database.models import Property
from src.config import FilterConfig

def filter_property(property: Property) -> bool:
    """Filter properties based on given criteria."""
    config = FilterConfig()
    
    # Handle None values in config
    min_price = config.min_price if config.min_price is not None else 0
    max_price = config.max_price if config.max_price is not None else float('inf')
    min_rooms = config.min_rooms if config.min_rooms is not None else 0
    max_rooms = config.max_rooms if config.max_rooms is not None else float('inf')
    min_size = config.min_size if config.min_size is not None else 0
    max_size = config.max_size if config.max_size is not None else float('inf')
    
    # Apply filters
    if property.price < min_price or property.price > max_price:
        return False
    
    if property.rooms < min_rooms or property.rooms > max_rooms:
        return False
        
    if property.size < min_size or property.size > max_size:
        return False
    
    # Add any other filtering logic here
    
    return True
