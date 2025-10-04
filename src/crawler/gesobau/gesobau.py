import asyncio
import json
from pathlib import Path
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, JsonCssExtractionStrategy
from src.crawler.base import BaseCrawler
from src.crawler.gesobau.extraction_schemas import GesobauExtractionSchema
from src.config import CrawlerConfig
from crawl4ai import CrawlResult
from typing import List, Optional
from database.models import Property
from src.utils.normalize_data import normalize_property
from src.utils.filter_property import filter_property
from src.utils.js_filter_generator import generate_js_filter_config


class GesobauCrawler(BaseCrawler):
    BASE_URL = "https://www.gesobau.de"
    SEARCH_URL = f"{BASE_URL}/mieten/wohnungssuche/"
     

    async def get_listing_urls(self) -> list[str]:
        strategy = JsonCssExtractionStrategy(schema=GesobauExtractionSchema.SCHEMA_LISTING_URLS)
        js_apply_filter = None
        js_file_path = Path(__file__).parent / "pre-filter.js"
        if self.crawler_config.pre_filter:
            js_config = generate_js_filter_config(self.filter_config)
            js_content = js_file_path.read_text(encoding='utf-8')
            js_apply_filter = js_config + "\n\n" + js_content
        all_links = set()
        async with AsyncWebCrawler() as crawler:
            result_initial: CrawlResult = await crawler.arun(
                url=self.SEARCH_URL,
                config=CrawlerRunConfig(
                    extraction_strategy=strategy,
                    js_code=js_apply_filter,
                    session_id="gesobau_session",
                    wait_for=GesobauExtractionSchema.WAIT_FOR_ELEMENT
                )
            )

            if result_initial.success:
                for prop in json.loads(result_initial.extracted_content):
                    all_links.add(prop.get('link'))
                print (f"Gesobau: Found {len(all_links)} links on initial page.")


            for _ in range(2, 26):
                result_next: CrawlResult = await crawler.arun(
                    url=self.SEARCH_URL,
                    config=CrawlerRunConfig(
                        extraction_strategy=strategy,
                        session_id="gesobau_session",
                        js_only=True,
                        js_code=GesobauExtractionSchema.NEXT_PAGE_SELECTOR_JS,
                        wait_for=GesobauExtractionSchema.WAIT_FOR_ELEMENT
                    )
                )
                if not result_next.success:
                    break

                new_links = {p.get('link') for p in json.loads(result_next.extracted_content) if p.get('link')}
                if not new_links or new_links.issubset(all_links):
                    break
                print (f"Gesobau: Found {len(new_links)} new links on next page.")
                all_links.update(new_links)

        all_urls = []

        print(f"Gesobau: Found {len(all_links)} unique listing URLs.")
        for link in all_links:
            all_urls.append(f"https://www.gesobau.de{link}" if not link.startswith('http') else link)
        return all_urls



    async def parse_listings(self, urls: list[str]) -> Optional[List[Property]]:
        strategy = JsonCssExtractionStrategy(schema=GesobauExtractionSchema.SCHEMA_SINGLE_PROPERTY)
        async with AsyncWebCrawler() as crawler:
            results: List[CrawlResult] = await crawler.arun_many(
                urls=urls,
                bypass_cache=True,
                config=CrawlerRunConfig(
                    extraction_strategy=strategy,
                    wait_for=GesobauExtractionSchema.WAIT_FOR_LISTING_ELEMENT,
                    page_timeout=15000
                )
            )

        properties: List[Property] = []
        failed_urls = []

        for result in results:
            if not result.success:
                failed_urls.append(result.url)
                print(f"Gesobau: Failed to crawl {result.url}: {result.error_message}")
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
                print(f"Gesobau: No valid data from {result.url}")

        print(f"Gesobau: Parsed {len(properties)}/{len(urls)} properties after filtering.")
        if failed_urls:
            print(f"Gesobau: Failed URLs ({len(failed_urls)}): {failed_urls}...")

        return properties


    
async def crawl(crawler_config: CrawlerConfig | None = None):
    cfg = crawler_config or CrawlerConfig()
    gesobau_crawler = GesobauCrawler(crawler_config=cfg)
    url_list = await gesobau_crawler.get_listing_urls()
    property_list = await gesobau_crawler.parse_listings(urls=url_list)
    return property_list


if __name__ == "__main__":
    properties = asyncio.run(crawl())