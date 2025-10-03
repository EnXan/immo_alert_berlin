from abc import ABC, abstractmethod
from typing import List, Optional
from src.config import CrawlerConfig
from database.models import Property
        
class BaseCrawler(ABC):
    """Abstract base class for all property crawlers"""

    def __init__(self, config: 'CrawlerConfig'):
        self.config = config
        self.source_name = self.__class__.__name__.replace('Crawler', '').lower()

    @abstractmethod
    async def get_listing_urls(self) -> list[str]:
        """Fetch all listing URLs from the search page"""
        pass

    @abstractmethod
    async def parse_listings(self, urls: list[str]) -> Optional[List[Property]]:
        """Parse all listing pages for given urls"""
        pass


    async def crawl(self) -> list[Property]:
        listing_urls = await self.get_listing_urls()
        #properties = await self.get_all_listing_details(listing_urls)
        #return properties


