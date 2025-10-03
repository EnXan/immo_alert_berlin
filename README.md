# 🏠 immo_alert

A smart automation tool that monitors multiple Berlin housing portals for new apartment listings and sends instant notifications via Telegram. Perfect for apartment hunters who want to be the first to know about new listings that match their criteria.

## 🎯 How it works

immo_alert automatically scrapes seven major Berlin housing companies every hour during business hours (Monday-Friday, 5 AM - 6 PM). The workflow:

1. **Parallel Crawling**: Simultaneously fetches listings from all portals using async operations
2. **Smart Filtering**: Applies pre-configured filters (2-3 rooms, max €900 warm rent)
3. **Change Detection**: Compares new results against a local JSON database
4. **Instant Notifications**: Sends Telegram messages for:
   - 🆕 New listings
   - 💰 Price changes
   - ❌ Removed listings (disabled by default to reduce noise)

The system maintains a complete history with timestamps, tracking when each listing first appeared and was last seen.

## 🛠️ Tools used

- **[crawl4ai](https://github.com/unclecode/crawl4ai)** (v0.7.4+) - Advanced async web scraping with JavaScript rendering
- **[uv](https://github.com/astral-sh/uv)** - Ultra-fast Python package manager for dependency management
- **Playwright** - Headless browser automation for dynamic content
- **GitHub Actions** - Automated scheduled runs with cron jobs
- **Telegram Bot API** - Real-time push notifications

### Architecture
```bash
src/
├── crawler/          # Individual scrapers per portal
│   ├── degewo.py
│   ├── gesobau.py
│   ├── gewobag.py
│   ├── howoge.py
│   ├── stadtundland.py
│   ├── vonovia.py
│   └── wbm.py
├── notification/     # Telegram integration
│   └── telegram.py
└── orchestrator.py   # Main coordination logic
database/
├── database.py       # Listing sync & change detection
└── database.json     # Persistent storage (Git-tracked)
```

## 🚀 How to start

### Prerequisites

- Python 3.12+
- uv package manager
- Telegram bot token & channel ID

### Local Setup

1. **Install uv**:
```bash
curl -LsSf https://astral.sh/uv install.sh | sh
```

2. **Clone & install dependencies:**
```bash
git clone <your-repo-url>
cd immo_alert
uv sync
uv run playwright install chromium
```

3. **Configure environment variables:**
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token"
export TELEGRAM_CHANNEL_ID="your_channel_id"
```

4. **Run manually:**
```bash
uv run python -m src.orchestrator
```

### GitHub Actions Setup (Automated)

1. __Add repository secrets__ (Settings → Secrets and variables → Actions):

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHANNEL_ID`


2. __Enable Actions__: The workflow in `.github/workflows/scraper.yml` will automatically run:

- Every hour from 5 AM - 6 PM (Mon-Fri)
- On manual trigger via Actions tab

3. __Database persistence__: Results are automatically committed back to the repo after each run.

### Creating a Telegram Bot

1. Message @BotFather on Telegram
2. Send /newbot and follow instructions
3. Copy the bot token
4. Add your bot to a channel and get the channel ID using @getidsbot


### Features
- Parallel Processing: All portals scraped simultaneously for speed
- WBS Detection: Automatically identifies if Wohnberechtigungsschein is required
- Price Tracking: Monitors price changes over time
- Duplicate Prevention: URL-based deduplication
- Rich Notifications: Formatted Telegram messages with direct links
- Zero Maintenance: Fully automated via GitHub Actions
- Git-based Storage: No external database required

### 🔧 Customization


### Changing Schedule
Modify the cron expression in `.github/workflows/scraper.yml`:

```bash
schedule:
  - cron: '0 5-18 * * 1-5'  # Currently: hourly, 5AM-6PM, Mon-Fri
```

### Adding New Portals
1. Create a new crawler in src/crawler/
2. Implement async def crawl() returning property list
3. Add to src/orchestrator.py:
```bash
from src.crawler import newportal
newportal_task = asyncio.create_task(newportal.crawl())
```


## 📝 License
MIT

## 🤝 Contributing

Contributions welcome! Especially for:

Additional Berlin housing portals
Improved CSS selectors when sites change
Enhanced notification formatting
Performance optimizations

## ⚠️ Disclaimer
This tool is for personal use only. Please respect the terms of service of the scraped websites and use responsibly. Consider adding delays and respecting robots.txt if running at higher frequencies.