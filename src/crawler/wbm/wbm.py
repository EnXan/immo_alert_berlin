import asyncio
import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, JsonCssExtractionStrategy
from src.crawler.base import BaseCrawler
from src.crawler.vonovia.vonovia import VonoviaCrawler
from src.crawler.wbm.extraction_schemas import WBMExtractionSchema
from src.config import CrawlerConfig
from crawl4ai import CrawlResult
from typing import List, Optional
from database.models import Property
from src.utils.normalize_data import normalize_property
from src.utils.filter_property import filter_property


class WBMCrawler(BaseCrawler):
    BASE_URL = "https://www.wbm.de"
    SEARCH_URL = f"{BASE_URL}/wohnungen-berlin/angebote/"
     

    async def get_listing_urls(self) -> list[str]:
        strategy = JsonCssExtractionStrategy(schema=WBMExtractionSchema.SCHEMA_LISTING_URLS)
        all_links = set()
        async with AsyncWebCrawler() as crawler:
            result_initial: CrawlResult = await crawler.arun(
                url=self.SEARCH_URL,
                config=CrawlerRunConfig(
                    extraction_strategy=strategy,
                    #js_code=WBMExtractionSchema.LISTING_URLS_PRE_FILTER_JS,
                    session_id="wbm_session",
                    wait_for=WBMExtractionSchema.WAIT_FOR_ELEMENT
                )
            )

            if result_initial.success:
                for prop in json.loads(result_initial.extracted_content):
                    all_links.add(prop.get('link'))


        all_urls = []

        print(f"WBM: Found {len(all_links)} unique listing URLs.")
        for link in all_links:
            all_urls.append(f"https://www.wbm.de{link}" if not link.startswith('http') else link)
        return all_urls



    async def parse_listings(self, urls: list[str]) -> Optional[List[Property]]:
        strategy = JsonCssExtractionStrategy(schema=WBMExtractionSchema.SCHEMA_SINGLE_PROPERTY)
        async with AsyncWebCrawler() as crawler:
            results: List[CrawlResult] = await crawler.arun_many(
                urls=urls,
                bypass_cache=True,
                config=CrawlerRunConfig(
                    extraction_strategy=strategy,
                    wait_for=WBMExtractionSchema.WAIT_FOR_LISTING_ELEMENT,
                    page_timeout=15000
                )
            )

        properties: List[Property] = []
        failed_urls = []

        for result in results:
            if not result.success:
                failed_urls.append(result.url)
                print(f"WBM: Failed to crawl {result.url}: {result.error_message}")
                continue 
                
            data = json.loads(result.extracted_content)
            if data and isinstance(data, list) and len(data) > 0:
                property = data[0]
                property["url"] = result.url
                property["source"] = self.source_name
                property = normalize_property(property)
                
                if filter_property(property, self.filter_config):
                    properties.append(property)
            else:
                print(f"WBM: No valid data from {result.url}")

        print(f"WBM: Parsed {len(properties)}/{len(urls)} properties after filtering.")
        if failed_urls:
            print(f"WBM: Failed URLs ({len(failed_urls)}): {failed_urls}...")

        return properties


    
async def crawl(crawler_config: CrawlerConfig | None = None):
    cfg = crawler_config or CrawlerConfig()
    wbm_crawler = WBMCrawler(crawler_config=cfg)
    url_list = await wbm_crawler.get_listing_urls()
    property_list = await wbm_crawler.parse_listings(urls=url_list)
    return property_list


if __name__ == "__main__":
    properties = asyncio.run(crawl())