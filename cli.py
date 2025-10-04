import asyncio
import click
from pathlib import Path


@click.group()
def cli():
    """ImmoAlert - Berlin apartment monitoring"""
    pass


@cli.command()
@click.option('--config', type=click.Path(exists=True), default='config.yaml', help='Config file path')
def run(config):
    """Run the crawler"""
    from src.orchestrator import ImmoAlert
    from src.config import AppConfig
    from src.crawler.degewo.degewo import DegewoCrawler
    from src.crawler.gewobag.gewobag import GewobagCrawler
    from src.crawler.gesobau.gesobau import GesobauCrawler
    from src.crawler.howoge.howoge import HowogeCrawler
    from src.crawler.stadtundland.stadtundland import StadtUndLandCrawler
    from src.crawler.vonovia.vonovia import VonoviaCrawler
    from src.crawler.wbm.wbm import WBMCrawler
    
    # Load config
    try:
        app_config = AppConfig.from_yaml(Path(config))
        print(f"✅ Loaded config from {config}")
    except FileNotFoundError:
        print(f"⚠️  Config file not found, using environment variables")
        app_config = AppConfig.from_env()
    
    # Initialize crawlers with filter config.
    # Respect `enabled_sources` from the loaded config (case-insensitive).
    crawler_classes = {
        'degewo': DegewoCrawler,
        'gewobag': GewobagCrawler,
        'gesobau': GesobauCrawler,
        'howoge': HowogeCrawler,
        'stadtundland': StadtUndLandCrawler,
        'vonovia': VonoviaCrawler,
        'wbm': WBMCrawler,
    }

    crawlers = []
    for name, cls in crawler_classes.items():
        if app_config.crawler.is_enabled(name):
            # pass both filter config and the shared crawler config
            crawlers.append(cls(app_config.filters, app_config.crawler))
        else:
            print(f"\u26a0\ufe0f  Skipping disabled crawler: {name}")
    
    app = ImmoAlert(crawlers, app_config)
    asyncio.run(app.run())


@cli.command()
def stats():
    """Show database statistics"""
    from src.orchestrator import ImmoAlert
    from src.config import AppConfig
    from pathlib import Path
    
    try:
        app_config = AppConfig.from_yaml(Path("config.yaml"))
    except FileNotFoundError:
        app_config = AppConfig.from_env()
    
    app = ImmoAlert([], app_config)
    app.stats()


@cli.command()
def test_telegram():
    """Test Telegram connection"""
    from src.notification.telegram import TelegramNotifier
    from database.models import StoredProperty
    from datetime import datetime
    
    notifier = TelegramNotifier()
    
    if not notifier.enabled:
        print("❌ Telegram not configured")
        print("Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL_ID environment variables")
        return
    
    print("📤 Sending test message...")
    
    test_prop = StoredProperty(
        title="Test Wohnung",
        url="https://test.de",
        address="Teststraße 1, 12345 Berlin",
        price=800.0,
        rooms=2.0,
        size=55.0,
        wbs_required=False,
        postal_code="12345",
        source="test",
        first_seen=datetime.now().isoformat(),
        last_seen=datetime.now().isoformat()
    )
    
    if notifier.send_new_property(test_prop):
        print("✅ Test message sent!")
    else:
        print("❌ Failed to send test message")


@cli.command()
@click.option('--source', help='Filter by source')
@click.option('--max-price', type=float, help='Maximum price')
@click.option('--min-rooms', type=float, help='Minimum rooms')
@click.option('--max-rooms', type=float, help='Maximum rooms')
def list(source, max_price, min_rooms, max_rooms):
    """List properties from database"""
    from database.database import PropertyDatabase
    
    db = PropertyDatabase()
    properties = db.load()
    
    # Filter
    filtered = [p for p in properties.values() if p.status == "active"]
    
    if source:
        filtered = [p for p in filtered if p.source == source]
    
    if max_price:
        filtered = [p for p in filtered if p.price <= max_price]
    
    if min_rooms:
        filtered = [p for p in filtered if p.rooms >= min_rooms]
    
    if max_rooms:
        filtered = [p for p in filtered if p.rooms <= max_rooms]
    
    print(f"\n📋 Found {len(filtered)} properties\n")
    
    for prop in filtered[:20]:  # Show first 20
        print(f"• {prop.title[:50]}")
        print(f"  {prop.address}")
        print(f"  {prop.price}€ • {prop.rooms} Zimmer • {prop.size}m²")
        if prop.source:
            print(f"  Source: {prop.source}")
        print(f"  {prop.url}")
        print()


@cli.command()
@click.confirmation_option(prompt='Are you sure you want to clear the database?')
def clear():
    """Clear the database"""
    db_path = Path("database/database.json")
    if db_path.exists():
        db_path.unlink()
        print("✅ Database cleared")
    else:
        print("ℹ️  Database already empty")


if __name__ == '__main__':
    cli()