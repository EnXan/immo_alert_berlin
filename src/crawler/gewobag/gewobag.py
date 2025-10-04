import asyncio
import json
from pathlib import Path
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, JsonCssExtractionStrategy
from src.crawler.base import BaseCrawler
from src.crawler.gewobag.extraction_schemas import GewobagExtractionSchema
from src.config import CrawlerConfig
from crawl4ai import CrawlResult
from typing import List, Optional
from database.models import Property

from src.utils.normalize_data import normalize_property
from src.utils.filter_property import filter_property
from src.utils.js_filter_generator import generate_js_filter_config


class GewobagCrawler(BaseCrawler):
    BASE_URL = "https://www.gewobag.de"
    SEARCH_URL = f"{BASE_URL}/fuer-mietinteressentinnen/mietangebote/?objekttyp%5B%5D=wohnung&gesamtmiete_von=&gesamtmiete_bis=&gesamtflaeche_von=&gesamtflaeche_bis=&zimmer_von=&zimmer_bis=&sort-by="
     

    async def get_listing_urls(self) -> list[str]:
        strategy = JsonCssExtractionStrategy(schema=GewobagExtractionSchema.SCHEMA_LISTING_URLS)
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
                    session_id="gewobag_session",
                    wait_for=GewobagExtractionSchema.WAIT_FOR_ELEMENT
                )
            )

            if result_initial.success:
                for prop in json.loads(result_initial.extracted_content):
                    all_links.add(prop.get('link'))
                print (f"Gewobag: Found {len(all_links)} links on initial page.")

        all_urls = []

        print(f"Gewobag: Found {len(all_links)} unique listing URLs.")
        for link in all_links:
            all_urls.append(f"https://www.gewobag.de{link}" if not link.startswith('http') else link)
        return all_urls



    async def parse_listings(self, urls: list[str]) -> Optional[List[Property]]:
        strategy = JsonCssExtractionStrategy(schema=GewobagExtractionSchema.SCHEMA_SINGLE_PROPERTY)
        async with AsyncWebCrawler() as crawler:
            results: List[CrawlResult] = await crawler.arun_many(
                urls=urls,
                bypass_cache=True,
                config=CrawlerRunConfig(
                    extraction_strategy=strategy,
                    wait_for=GewobagExtractionSchema.WAIT_FOR_LISTING_ELEMENT,
                    page_timeout=15000
                )
            )

        properties: List[Property] = []
        failed_urls = []

        for result in results:
            if not result.success:
                failed_urls.append(result.url)
                print(f"Gewobag: Failed to crawl {result.url}: {result.error_message}")
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
                print(f"Gewobag: No valid data from {result.url}")

        print(f"Gewobag: Parsed {len(properties)}/{len(urls)} properties after filtering.")
        if failed_urls:
            print(f"Gewobag: Failed URLs ({len(failed_urls)}): {failed_urls}...")

        return properties


    
async def crawl(crawler_config: CrawlerConfig | None = None):
    cfg = crawler_config or CrawlerConfig()
    gewobag_crawler = GewobagCrawler(crawler_config=cfg)
    url_list = await gewobag_crawler.get_listing_urls()
    property_list = await gewobag_crawler.parse_listings(urls=url_list)
    return property_list


if __name__ == "__main__":
    properties = asyncio.run(crawl())