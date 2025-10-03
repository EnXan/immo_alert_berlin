import asyncio
import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, JsonCssExtractionStrategy
from src.crawler.base import BaseCrawler
from src.crawler.vonovia.extraction_schemas import VonoviaExtractionSchema
from src.config import CrawlerConfig
from crawl4ai import CrawlResult
from typing import List, Optional
from src.crawler.base import Property
from src.utils.normalize_data import normalize_property
from src.utils.filter_property import filter_property


class VonoviaCrawler(BaseCrawler):
    BASE_URL = "https://www.vonovia.de"
    SEARCH_URL = f"{BASE_URL}/zuhause-finden/immobilien?rentType=miete&city=Berlin&lift=0&parking=0&cellar=0&immoType=wohnung&priceMax=700&minRooms=0&floor=Beliebig&bathtub=0&bathwindow=0&bathshower=0&furnished=0&kitchenEBK=0&toiletSeparate=0&disabilityAccess=egal&seniorFriendly=0&balcony=egal&garden=0&subsidizedHousingPermit=egal&scroll=true"
     

    async def get_listing_urls(self) -> list[str]:
        strategy = JsonCssExtractionStrategy(schema=VonoviaExtractionSchema.SCHEMA_LISTING_URLS)
        all_links = set()
        async with AsyncWebCrawler() as crawler:
            result_initial: CrawlResult = await crawler.arun(
                url=self.SEARCH_URL,
                config=CrawlerRunConfig(
                    extraction_strategy=strategy,
                    #js_code=VonoviaExtractionSchema.LISTING_URLS_PRE_FILTER_JS,
                    session_id="vonovia_session",
                    wait_for=VonoviaExtractionSchema.WAIT_FOR_ELEMENT
                )
            )

            if result_initial.success:
                for prop in json.loads(result_initial.extracted_content):
                    all_links.add(prop.get('link'))


        all_urls = []

        print(f"Vonovia: Found {len(all_links)} unique listing URLs.")
        for link in all_links:
            all_urls.append(f"https://www.vonovia.de{link}" if not link.startswith('http') else link)
        return all_urls



    async def parse_listings(self, urls: list[str]) -> Optional[List[Property]]:
        strategy = JsonCssExtractionStrategy(schema=VonoviaExtractionSchema.SCHEMA_SINGLE_PROPERTY)
        async with AsyncWebCrawler() as crawler:
            results: List[CrawlResult] = await crawler.arun_many(
                urls=urls,
                bypass_cache=True,
                config=CrawlerRunConfig(
                    extraction_strategy=strategy,
                    wait_for=VonoviaExtractionSchema.WAIT_FOR_LISTING_ELEMENT,
                )
            )

        properties: List[Property] = []
        failed_urls = []

        for result in results:
            if not result.success:
                failed_urls.append(result.url)
                print(f"Vonovia: Failed to crawl {result.url}: {result.error_message}")
                continue 
                
            data = json.loads(result.extracted_content)
            if data and isinstance(data, list) and len(data) > 0:
                property = data[0]
                property["url"] = result.url
                property["source"] = self.source_name
                property = normalize_property(property)
                
                if filter_property(property):
                    properties.append(property)
            else:
                print(f"Vonovia: No valid data from {result.url}")

        print(f"Vonovia: Parsed {len(properties)}/{len(urls)} properties after filtering.")
        if failed_urls:
            print(f"Vonovia: Failed URLs ({len(failed_urls)}): {failed_urls}...")

        return properties


    
async def crawl():
    vonovia_crawler = VonoviaCrawler(config=CrawlerConfig())
    url_list = await vonovia_crawler.get_listing_urls()
    property_list = await vonovia_crawler.parse_listings(urls=url_list)
    return property_list


if __name__ == "__main__":
    properties = asyncio.run(crawl())