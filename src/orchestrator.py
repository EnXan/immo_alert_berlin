# src/orchestrator.py
import asyncio
from typing import List
from database.database import PropertyDatabase
from database.models import Property
from src.notification.telegram import TelegramNotifier


class ImmoAlert:
    """Main orchestrator"""
    
    def __init__(self, crawlers: List, db_path: str = "database/database.json"):
        self.crawlers = crawlers
        self.db = PropertyDatabase(db_path)
        self.notifier = TelegramNotifier()
        
        print(f"🚀 ImmoAlert initialized with {len(crawlers)} crawler(s)")
    
    async def run(self) -> None:
        """Run the full cycle"""
        print("\n" + "="*60)
        print("🏠 Starting ImmoAlert")
        print("="*60)
        
        # 1. Crawl all sources
        properties = await self._crawl_all()
        print(f"\n📥 Collected {len(properties)} properties total")
        
        # 2. Sync with database
        result = self.db.sync(properties)
        
        # 3. Send notifications
        self._notify(result)
        
        # 4. Summary
        print("\n" + "="*60)
        print("✅ Run complete!")
        print(f"   New: {len(result['new'])}, Updated: {len(result['updated'])}, Removed: {len(result['removed'])}")
        print("="*60 + "\n")
    
    async def _crawl_all(self) -> List[Property]:
        """Crawl all sources in parallel"""
        print("\n🔍 Starting crawlers...")
        
        tasks = []
        for crawler in self.crawlers:
            tasks.append(self._crawl_one(crawler))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Flatten results
        all_properties = []
        for result in results:
            if isinstance(result, Exception):
                print(f"❌ Crawler failed: {result}")
            elif isinstance(result, list):
                all_properties.extend(result)
        
        return all_properties
    
    async def _crawl_one(self, crawler) -> List[Property]:
        """Crawl single source"""
        name = crawler.__class__.__name__.replace('Crawler', '')
        print(f"  ⏳ {name}...")
        
        try:
            properties = await crawler.crawl()
            print(f"  ✅ {name}: {len(properties)} properties")
            return properties
        except Exception as e:
            print(f"  ❌ {name} failed: {e}")
            return []
    
    def _notify(self, result: dict) -> None:
        """Send notifications"""
        if not self.notifier.enabled:
            print("\n⚠️  Notifications disabled")
            return
        
        print("\n📤 Sending notifications...")
        
        # New properties
        for prop in result['new']:
            if self.notifier.send_new_property(prop):
                print(f"  ✅ Sent: New property")
            else:
                print(f"  ❌ Failed: New property")
        
        # Price updates
        for update in result['updated']:
            if self.notifier.send_price_update(update):
                print(f"  ✅ Sent: Price update")
            else:
                print(f"  ❌ Failed: Price update")
        
        # Removed (optional - disabled by default)
        # for prop in result['removed']:
        #     self.notifier.send_removed_property(prop)
    
    def stats(self) -> None:
        """Print statistics"""
        stats = self.db.get_stats()
        
        print("\n" + "="*60)
        print("📊 Statistics")
        print("="*60)
        print(f"Total properties:  {stats['total']}")
        print(f"Active:            {stats['active']}")
        print(f"Removed:           {stats['removed']}")
        print("\nBy source:")
        for source, count in stats['by_source'].items():
            print(f"  • {source.ljust(15)}: {count}")
        print("="*60 + "\n")