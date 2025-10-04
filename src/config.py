from dataclasses import dataclass, field
from typing import Optional, List
from pathlib import Path
import yaml
import os

@dataclass
class FilterConfig:
    """Filtering criteria"""
    min_rooms: Optional[float] = None
    max_rooms: Optional[float] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    min_size: Optional[float] = None
    max_size: Optional[float] = None
    wbs_required: Optional[bool] = None
    postal_codes: List[str] = field(default_factory=list)
    districts: List[str] = field(default_factory=list)
    
    def get_all_postal_codes(self) -> List[str]:
        """Get all postal codes from both direct postal_codes and districts."""
        from src.utils.berlin_districts import get_postal_codes_for_districts
        
        # Handle None values from YAML
        postal_codes = self.postal_codes or []
        districts = self.districts or []
        
        all_codes = set(postal_codes)
        
        # Add postal codes from districts
        if districts:
            district_codes = get_postal_codes_for_districts(districts)
            all_codes.update(district_codes)
        
        return sorted(list(all_codes))

@dataclass
class CrawlerConfig:
    """Per-crawler configuration"""
    enabled_sources: List[str] = field(default_factory=lambda: [
        'degewo', 'gesobau', 'gewobag', 'howoge', 
        'stadtundland', 'vonovia', 'wbm'
    ])
    
    def is_enabled(self, source: str) -> bool:
        """Check if a crawler source is enabled"""
        return source.lower() in [s.lower() for s in self.enabled_sources]
    
    pre_filter: bool = True

@dataclass
class NotificationConfig:
    """Notification settings"""
    telegram_enabled: bool = True
    telegram_bot_token: Optional[str] = None
    telegram_channel_id: Optional[str] = None
    notify_new_listings: bool = True
    notify_price_changes: bool = True
    notify_removals: bool = False

@dataclass
class AppConfig:
    """Main application configuration"""
    filters: FilterConfig
    crawler: CrawlerConfig
    notification: NotificationConfig
    database_path: Path = Path("database/database.json")

    @classmethod
    def from_yaml(cls, path: Path) -> 'AppConfig':
        """Load config from YAML file"""
        with open(path) as f:
            data = yaml.safe_load(f)

        # Handle None values from YAML for list fields
        filters_data = data.get('filters', {})
        if 'postal_codes' in filters_data and filters_data['postal_codes'] is None:
            filters_data['postal_codes'] = []
        if 'districts' in filters_data and filters_data['districts'] is None:
            filters_data['districts'] = []

        return cls(
            filters=FilterConfig(**filters_data),
            crawler=CrawlerConfig(**data.get('crawler', {})),
            notification=NotificationConfig(**data.get('notification', {})),
            database_path=Path(data.get('database_path', 'database/database.json'))
        )
    
    @classmethod
    def from_env(cls) -> 'AppConfig':
        """Load config from environment variables"""
        return cls(
            filters=FilterConfig(
                min_rooms=float(os.getenv("MIN_ROOMS", 0)) if os.getenv("MIN_ROOMS") else None,
                max_rooms=float(os.getenv("MAX_ROOMS", 10)) if os.getenv("MAX_ROOMS") else None,
                min_price=float(os.getenv("MIN_PRICE", 0)) if os.getenv("MIN_PRICE") else None,
                max_price=float(os.getenv("MAX_PRICE", 1500)) if os.getenv("MAX_PRICE") else None,
            ),
            crawler=CrawlerConfig(),
            notification=NotificationConfig(
                telegram_bot_token=os.getenv('TELEGRAM_BOT_TOKEN'),
                telegram_channel_id=os.getenv('TELEGRAM_CHANNEL_ID')
            )
        )