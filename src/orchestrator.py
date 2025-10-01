from src.crawler.degewo import crawl
import asyncio
from database.database import ListingDatabase
from src.notification.telegram import TelegramNotifier
import os

def check_new_properties():
    db = ListingDatabase()
    properties =  asyncio.run(crawl())
    print(f"Crawled {len(properties)} properties.")
    results = db.sync_listings(properties)
    return results

def notify_via_telegram(results):
    channel_id = os.getenv('TELEGRAM_CHANNEL_ID')
    notifier = TelegramNotifier(channel_id)
    for listing in results['new']:
        notifier.send_new_listing(listing)
    for listing in results['removed']:
        notifier.send_removed_listing(listing)
    for update in results['updated']:
        notifier.send_price_update(update)
    notifier.send_summary(results)

if __name__ == "__main__":
    results = check_new_properties()
    notify_via_telegram(results)