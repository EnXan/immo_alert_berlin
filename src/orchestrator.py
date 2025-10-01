from src.crawler import degewo, gesobau, gewobag, howoge, wbm

import asyncio
from database.database import ListingDatabase
from src.notification.telegram import TelegramNotifier
import os

async def crawl_all_parallel():
    # Führe Degewo und Gesobau parallel aus
    degewo_task = asyncio.create_task(degewo.crawl())
    gesobau_task = asyncio.create_task(gesobau.crawl())
    gewobag_task = asyncio.create_task(gewobag.crawl())
    howoge_task = asyncio.create_task(howoge.crawl())
    wbm_task = asyncio.create_task(wbm.crawl())
    
    # Warte auf beide Ergebnisse
    properties_degewo, properties_gesobau, properties_gewobag, properties_howoge, properties_wbm = await asyncio.gather(degewo_task, gesobau_task, gewobag_task, howoge_task, wbm_task)

    return properties_degewo + properties_gesobau + properties_gewobag + properties_howoge + properties_wbm 

def check_new_properties():
    db = ListingDatabase()
    properties = asyncio.run(crawl_all_parallel())
    
    # Filtere defekte Properties heraus
    valid_properties = []
    for prop in properties:
        # Prüfe ob alle erforderlichen Felder vorhanden sind
        if prop.get('title') and prop.get('url'):
            valid_properties.append(prop)
        else:
            print(f"Skipping invalid property: {prop}")
    
    print(f"Crawled {len(properties)} properties, {len(valid_properties)} valid.")
    results = db.sync_listings(valid_properties)
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