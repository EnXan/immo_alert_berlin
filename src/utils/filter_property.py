from database.models import Property
from src.config import FilterConfig

def filter_property(property: Property, config: FilterConfig = None) -> bool:
    """Filter properties based on given criteria."""
    if config is None:
        config = FilterConfig()  # Use defaults if no config provided
    
    # Price filter
    if config.min_price is not None and property.price < config.min_price:
        return False
    if config.max_price is not None and property.price > config.max_price:
        return False
    
    # Rooms filter
    if config.min_rooms is not None and property.rooms < config.min_rooms:
        return False
    if config.max_rooms is not None and property.rooms > config.max_rooms:
        return False
    
    # Size filter
    if config.min_size is not None and property.size < config.min_size:
        return False
    if config.max_size is not None and property.size > config.max_size:
        return False
    
    # WBS filter (if specified)
    if config.wbs_required is not None:
        if property.wbs_required != config.wbs_required:
            return False
    
    return True