"""
Utility to generate JavaScript filter configurations for web crawlers.
"""

from src.config import FilterConfig


def generate_js_filter_config(filter_config: FilterConfig) -> str:
    """
    Generate a JavaScript object string with filter configuration values.
    
    Args:
        filter_config: The filter configuration object
        
    Returns:
        JavaScript code string defining a 'f' object with filter values
    """
    def js_value(value):
        """Convert Python value to JavaScript value string"""
        if value is None:
            return "null"
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, str):
            return f'"{value}"'
        else:
            return "null"
    
    js_config = f"""
// Auto-generated filter configuration
const f = {{
    min_rooms: {js_value(filter_config.min_rooms)},
    max_rooms: {js_value(filter_config.max_rooms)},
    min_price: {js_value(filter_config.min_price)},
    max_price: {js_value(filter_config.max_price)},
    min_size: {js_value(filter_config.min_size)},
    max_size: {js_value(filter_config.max_size)},
    wbs_required: {js_value(filter_config.wbs_required)}
}};
"""
    return js_config.strip()