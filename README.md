# Immo Alert Berlin

![Immo Alert](logo.png)

A smart automation tool that monitors multiple Berlin housing portals for new apartment listings and sends instant notifications via Telegram. Perfect for apartment hunters who want to be the first to know about new listings that match their criteria.

## 🎯 How it works

immo_alert automatically scrapes seven major Berlin housing companies and compares results against a local database. The workflow:

1. **Parallel Crawling**: Simultaneously fetches listings from all portals using async operations
2. **Smart Filtering**: Applies configurable filters (rooms, price, size, WBS requirements)
3. **Change Detection**: Compares new results against a local JSON database
4. **Instant Notifications**: Sends Telegram messages for:
   - 🆕 New listings
   - 💰 Price changes
   - ❌ Removed listings (optional, disabled by default)

The system maintains a complete history with timestamps, tracking when each listing first appeared and was last seen.

## 🛠️ Tools used

- **[crawl4ai](https://github.com/unclecode/crawl4ai)** (v0.7.4+) - Advanced async web scraping with JavaScript rendering
- **[uv](https://github.com/astral-sh/uv)** - Ultra-fast Python package manager
- **Playwright** - Headless browser automation for dynamic content
- **Click** - Beautiful command-line interface
- **GitHub Actions** - Automated scheduled runs (optional)
- **Telegram Bot API** - Real-time push notifications

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Telegram account (for notifications)

### 1. Install uv (if not already installed)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clone and setup

```bash
git clone https://github.com/yourusername/immo_alert.git
cd immo_alert

# Install dependencies
uv sync

# Install Playwright browser
uv run playwright install chromium
uv run playwright install-deps chromium
```

### 3. Create Telegram Bot

1. Open Telegram and message [@BotFather](https://t.me/botfather)
2. Send `/newbot` and follow instructions
3. Copy the **bot token** (looks like `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)
4. Create a channel or group for notifications
5. Add your bot to the channel/group as administrator
6. Get your channel/chat ID using [@getidsbot](https://t.me/getidsbot)
   - Forward any message from your channel to @getidsbot
   - It will reply with the chat ID (looks like `-1001234567890`)

### 4. Configure the application

Create `config.yaml` in the project root:

```yaml
# config.yaml
filters:
  min_rooms: 2 # Minimum number of rooms
  max_rooms: 3 # Maximum number of rooms
  min_price: null # Minimum price (null = no limit)
  max_price: 900 # Maximum price in EUR (warm)
  min_size: null # Minimum size in m²
  max_size: null # Maximum size in m²
  wbs_required: null # null = don't care, true = only with WBS, false = only without WBS

crawler:
  enabled_sources: # List of crawler sources to use
    - degewo
    - gesobau
    - gewobag
    - howoge
    - stadtundland
    - vonovia
    - wbm
  pre_filter: true # uses js to actually click the filter settings on the websites if available. This makes the crawling faster. If it fails just deactivate it

notification:
  telegram_enabled: true
  notify_new_listings: true
  notify_price_changes: true
  notify_removals: false # Set to true if you want removal notifications

database_path: "database/database.json"
```

Then set your Telegram credentials as environment variables:

```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export TELEGRAM_CHANNEL_ID="your_channel_id_here"
```

**For permanent setup**, add to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
# Add these lines to ~/.bashrc or ~/.zshrc
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export TELEGRAM_CHANNEL_ID="your_channel_id_here"
```

### 5. Test your setup

```bash
# Test Telegram connection
uv run python cli.py test-telegram

# If successful, you should see:
# 📤 Sending test message...
# ✅ Test message sent!
```

### 6. Run your first crawl

```bash
# Run with config file
uv run python cli.py run

# You should see:
# ✅ Loaded config from config.yaml
#   ✅ Enabled: degewo
#   ✅ Enabled: gesobau
#   ...
# 🚀 Starting with 7 crawler(s)
```

## 📋 CLI Commands

### Main Commands

```bash
# Run the crawler
uv run python cli.py run

# Show database statistics
uv run python cli.py stats

# List active properties
uv run python cli.py list

# Test Telegram notifications
uv run python cli.py test-telegram

# Clear database (requires confirmation)
uv run python cli.py clear
```

### Filtering listings

```bash
# Filter by source
uv run python cli.py list --source degewo

# Filter by price
uv run python cli.py list --max-price 800

# Filter by rooms
uv run python cli.py list --min-rooms 2 --max-rooms 3

# Combine filters
uv run python cli.py list --source howoge --max-price 700 --min-rooms 2
```

## ⚙️ Configuration Guide

### Filter Options

| Option         | Type      | Description             | Example                                                 |
| -------------- | --------- | ----------------------- | ------------------------------------------------------- |
| `min_rooms`    | float     | Minimum number of rooms | `2`                                                     |
| `max_rooms`    | float     | Maximum number of rooms | `3`                                                     |
| `min_price`    | float     | Minimum rent in EUR     | `500`                                                   |
| `max_price`    | float     | Maximum rent in EUR     | `900`                                                   |
| `min_size`     | float     | Minimum size in m²      | `45`                                                    |
| `max_size`     | float     | Maximum size in m²      | `80`                                                    |
| `wbs_required` | bool/null | WBS requirement filter  | `null` (any), `true` (required), `false` (not required) |

### Crawler Configuration

Enable or disable specific crawlers in your `config.yaml`:

```yaml
crawler:
  enabled_sources:
    - degewo # ✅ Enabled
    - gesobau # ✅ Enabled
    - gewobag # ✅ Enabled
    - howoge # ✅ Enabled
    - stadtundland # ✅ Enabled
    - vonovia # ✅ Enabled
    - wbm # ✅ Enabled
```

**Available sources:**

- `degewo` - Degewo
- `gesobau` - GESOBAU
- `gewobag` - Gewobag
- `howoge` - HOWOGE
- `stadtundland` - Stadt und Land
- `vonovia` - Vonovia
- `wbm` - WBM

**Example: Only fast crawlers**

```yaml
crawler:
  enabled_sources:
    - degewo
    - gewobag
    - wbm
```

**Example: Test single crawler**

```yaml
crawler:
  enabled_sources:
    - degewo # Only test Degewo
```

This allows you to:

- ✅ Test individual crawlers
- ✅ Disable slow or problematic sources
- ✅ Focus on specific housing companies
- ✅ Reduce runtime for faster iterations

### Environment Variables

| Variable              | Required | Description                            |
| --------------------- | -------- | -------------------------------------- |
| `TELEGRAM_BOT_TOKEN`  | Yes      | Your Telegram bot token from BotFather |
| `TELEGRAM_CHANNEL_ID` | Yes      | Your channel/chat ID (starts with `-`) |
| `MIN_ROOMS`           | No       | Override min_rooms from config         |
| `MAX_ROOMS`           | No       | Override max_rooms from config         |
| `MAX_PRICE`           | No       | Override max_price from config         |

**Note**: Environment variables take precedence over config file settings.

## 🤖 Automation with GitHub Actions

### Setup Automated Runs

1. **Fork this repository** to your GitHub account

2. **Add secrets** to your repository:

   - Go to: Settings → Secrets and variables → Actions → New repository secret
   - Add `TELEGRAM_BOT_TOKEN`
   - Add `TELEGRAM_CHANNEL_ID`

3. **Enable GitHub Actions**:

   - Go to the Actions tab
   - Click "I understand my workflows, go ahead and enable them"

4. **Customize schedule** (optional):

   Edit `.github/workflows/scraper.yml`:

   ```yaml
   on:
     schedule:
       - cron: "0 5-18 * * 1-5" # Every hour, 5AM-6PM, Mon-Fri
   ```

5. **Manual trigger**:
   - Go to Actions tab → "Wohnungs Scraper" → Run workflow

### How it works

- Runs automatically based on your schedule
- Results are committed back to the repository
- Database persists between runs
- Sends notifications for any changes

## 🏢 Monitored Housing Portals

| Portal                                    | Status    | Default Filters |
| ----------------------------------------- | --------- | --------------- |
| [Degewo](https://www.degewo.de)           | ✅ Active | Configurable    |
| [GESOBAU](https://www.gesobau.de)         | ✅ Active | Configurable    |
| [Gewobag](https://www.gewobag.de)         | ✅ Active | Configurable    |
| [HOWOGE](https://www.howoge.de)           | ✅ Active | Configurable    |
| [Stadt und Land](https://stadtundland.de) | ✅ Active | Configurable    |
| [WBM](https://www.wbm.de)                 | ✅ Active | Configurable    |
| [Vonovia](https://www.vonovia.de)         | ✅ Active | Configurable    |

## 📊 Project Structure

```
immo_alert/
├── .github/workflows/
│   └── scraper.yml          # GitHub Actions workflow
├── database/
│   ├── database.json        # Property database (git-tracked)
│   ├── database.py          # Database management
│   └── models.py            # Data models
├── src/
│   ├── crawler/
│   │   ├── base.py          # Base crawler class
│   │   ├── degewo/          # Degewo-specific crawler
│   │   ├── gesobau/         # Gesobau-specific crawler
│   │   ├── gewobag/         # Gewobag-specific crawler
│   │   ├── howoge/          # Howoge-specific crawler
│   │   ├── stadtundland/    # Stadt und Land crawler
│   │   ├── vonovia/         # Vonovia crawler
│   │   └── wbm/             # WBM crawler
│   ├── notification/
│   │   └── telegram.py      # Telegram notifications
│   ├── utils/
│   │   ├── filter_property.py    # Property filtering
│   │   └── normalize_data.py     # Data normalization
│   ├── config.py            # Configuration management
│   └── orchestrator.py      # Main coordination logic
├── cli.py                   # Command-line interface
├── config.yaml              # Configuration file (create this)
├── pyproject.toml           # Project dependencies
└── README.md                # This file
```

## 🔧 Troubleshooting

### "Failed to load database" error

If you see an error about missing `source` field:

```bash
# Clear and restart (recommended)
uv run python cli.py clear
uv run python cli.py run
```

### Telegram notifications not working

```bash
# Test your Telegram setup
uv run python cli.py test-telegram

# Check your environment variables are set
echo $TELEGRAM_BOT_TOKEN
echo $TELEGRAM_CHANNEL_ID

# If empty, set them:
export TELEGRAM_BOT_TOKEN="your_token"
export TELEGRAM_CHANNEL_ID="your_id"
```

### No properties found

This is normal! It means:

- ✅ Crawlers are working
- ✅ Filters are applied correctly
- ❌ No properties match your criteria right now

Try adjusting your filters in `config.yaml`:

- Increase `max_price`
- Increase `max_rooms`
- Set `wbs_required: null` (accept both with/without WBS)

### Crawler fails or times out

Some crawlers may be temporarily unavailable. You can:

1. **Disable problematic crawlers**:

   ```yaml
   crawler:
     enabled_sources:
       - degewo
       - gewobag
       # - howoge  # Temporarily disabled
   ```

2. **Run again later** - websites may be temporarily down

3. **Check if website structure changed** - CSS selectors may need updates

## 📈 Tips for Success

1. **Run regularly**: Properties appear and disappear quickly. Run every hour during business hours.

2. **Adjust filters gradually**: Start with broader filters, then narrow down.

3. **Monitor multiple sources**: Different companies have different availability.

4. **Act fast**: When you get a notification, check it immediately!

5. **Use GitHub Actions**: Automate the process so you never miss a listing.

## 🤝 Contributing

Contributions are welcome! Especially for:

- Additional Berlin housing portals
- Improved CSS selectors when sites change
- Enhanced notification formatting
- Performance optimizations
- New configurations
- Bug fixes

To contribute:

```bash
# Fork the repo
git clone https://github.com/yourusername/immo_alert.git
cd immo_alert

# Create a branch
git checkout -b feature/your-feature

# Make your changes
# ...

# Test your changes
uv run python cli.py run

# Commit and push
git add .
git commit -m "Add your feature"
git push origin feature/your-feature
```

Then open a Pull Request!

## 📝 License

MIT License - feel free to use this tool for your apartment hunt!

## ⚠️ Disclaimer

This tool is for **personal use only**. Please:

- ✅ Respect the terms of service of scraped websites
- ✅ Use reasonable crawl intervals (don't spam)
- ✅ Consider the `robots.txt` files
- ❌ Don't use for commercial purposes
- ❌ Don't overload the servers

**Note**: Web scraping may be against some websites' ToS. Use at your own risk and responsibility.

## 🙏 Acknowledgments

- [crawl4ai](https://github.com/unclecode/crawl4ai) - Awesome web scraping framework
- [uv](https://github.com/astral-sh/uv) - Fast Python package manager
- All the Berlin housing companies for (unknowingly) providing the data

---

**Good luck with your apartment hunt! 🏠🔑**

_Found this helpful? Star the repo ⭐ and share with friends looking for apartments in Berlin!_
