import asyncio
import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, JsonCssExtractionStrategy
from src.crawler.base import BaseCrawler
from src.crawler.stadtundland.extraction_schemas import StadtUndLandExtractionSchema
from src.config import CrawlerConfig
from crawl4ai import CrawlResult
from typing import List, Optional
from database.models import Property
from src.utils.normalize_data import normalize_property
from src.utils.filter_property import filter_property
import re


class StadtUndLandCrawler(BaseCrawler):
    BASE_URL = "https://stadtundland.de"
    SEARCH_URL = f"{BASE_URL}/wohnungssuche/"
     

    async def get_listing_urls(self) -> list[str]:
        # Not working properly due to unknown reason there using markdown extraction
        #strategy = JsonCssExtractionStrategy(schema=StadtUndLandExtractionSchema.SCHEMA_LISTING_URLS)
        markdown_extraction_pattern = r'https://stadtundland\.de/wohnungssuche/(?!#)[^\s\)]+(?=%2F|\)|\s|$)'
        js_apply_filter = StadtUndLandExtractionSchema.LISTING_URLS_PRE_FILTER_JS #TODO: Muss noch dynamisch an Filter angepasst werden
        all_links = set()
        async with AsyncWebCrawler() as crawler:
            result_initial: CrawlResult = await crawler.arun(
                url=self.SEARCH_URL,
                config=CrawlerRunConfig(
                    #extraction_strategy=strategy,
                    #js_code=StadtUndLandExtractionSchema.LISTING_URLS_PRE_FILTER_JS,
                    session_id="stadtundland_session",
                    wait_for=StadtUndLandExtractionSchema.WAIT_FOR
                )
            )

            if result_initial.success:
                markdown_content = result_initial.markdown
                found_links = re.findall(markdown_extraction_pattern, markdown_content)

                for link in found_links:
                    # Clean up the link (remove URL encoding if needed)
                    clean_link = link.replace('%2F', '/')
                    all_links.add(clean_link)

            for load_attempt in range(1, 20): 
                result_next: CrawlResult = await crawler.arun(
                    url=self.SEARCH_URL,
                    config=CrawlerRunConfig(
                        session_id="stadtundland_session",
                        #extraction_strategy=strategy,
                        js_code=StadtUndLandExtractionSchema.LOAD_MORE_JS,
                        js_only=True,
                        wait_for=StadtUndLandExtractionSchema.WAIT_FOR
                    )
                )

                if not result_next.success:
                        break
                
                markdown_content = result_next.markdown
                found_links = re.findall(markdown_extraction_pattern, markdown_content)

                new_links = set()
                for link in found_links:
                    # Clean up the link (remove URL encoding if needed)
                    clean_link = link.replace('%2F', '/')
                    new_links.add(clean_link)
                
                if not new_links or new_links.issubset(all_links):
                    break
                all_links.update(new_links)

        all_urls = []

        print(f"StadtUndLand: Found {len(all_links)} unique listing URLs.")
        for link in all_links:
            all_urls.append(f"https://www.stadtundland.de{link}" if not link.startswith('http') else link)
        return all_urls



    async def parse_listings(self, urls: list[str]) -> Optional[List[Property]]:
        strategy = JsonCssExtractionStrategy(schema=StadtUndLandExtractionSchema.SCHEMA_SINGLE_PROPERTY)
        async with AsyncWebCrawler() as crawler:
            results: List[CrawlResult] = await crawler.arun_many(
                urls=urls,
                bypass_cache=True,
                config=CrawlerRunConfig(
                    extraction_strategy=strategy,
                    wait_for=StadtUndLandExtractionSchema.WAIT_FOR_LISTING_ELEMENT,
                    page_timeout=15000
                )
            )

        properties: List[Property] = []
        failed_urls = []

        for result in results:
            if not result.success:
                failed_urls.append(result.url)
                print(f"StadtUndLand: Failed to crawl {result.url}: {result.error_message}")
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
                print(f"StadtUndLand: No valid data from {result.url}")

        print(f"StadtUndLand: Parsed {len(properties)}/{len(urls)} properties after filtering.")
        if failed_urls:
            print(f"StadtUndLand: Failed URLs ({len(failed_urls)}): {failed_urls}...")

        return properties


    
async def crawl():
    stadtundland_crawler = StadtUndLandCrawler(config=CrawlerConfig())
    url_list = await stadtundland_crawler.get_listing_urls()
    property_list = await stadtundland_crawler.parse_listings(urls=url_list)
    return property_list


if __name__ == "__main__":
    properties = asyncio.run(crawl())