import requests
import os
from datetime import datetime

class TelegramNotifier:
    def __init__(self, channel_id, bot_token=None):
        self.bot_token = bot_token or os.getenv('TELEGRAM_BOT_TOKEN')
        if not self.bot_token:
            raise ValueError("Bot token must be provided either as parameter or via TELEGRAM_BOT_TOKEN environment variable")
        self.chat_id = channel_id
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"

    def send_new_listing(self, listing):
        wbs_status = "✅ Ja" if listing.get('wbs_required') == 'Ja' else "❌ Nein" if listing.get('wbs_required') == 'Nein' else listing.get('wbs_required', 'Nicht verfügbar')
        
        message = f"""🆕 <b>NEUE WOHNUNG GEFUNDEN!</b>

<pre>📍 Objekt:        {listing.get('title', 'Nicht verfügbar')}

📌 Adresse:       {listing.get('address', 'Nicht verfügbar')}

💰 Preis:         {listing.get('price', 'Nicht verfügbar')}

🏠 Details:       {listing.get('rooms', 'Nicht verfügbar')} Zimmer • {listing.get('size', 'Nicht verfügbar')}

🎫 WBS benötigt:  {wbs_status}</pre>

🔗 <b><a href="{listing.get('url', '#')}">» Jetzt ansehen «</a></b>"""
        return self._send_message(message)
    
    def send_removed_listing(self, listing):
        # Formatiere das Datum für bessere Lesbarkeit
        first_seen_formatted = 'Nicht verfügbar'
        if listing.get('first_seen'):
            try:
                dt = datetime.fromisoformat(listing['first_seen'])
                first_seen_formatted = dt.strftime('%d.%m.%Y um %H:%M Uhr')
            except ValueError:
                first_seen_formatted = listing.get('first_seen', 'Nicht verfügbar')
        
        message = f"""❌ <b>WOHNUNG NICHT MEHR VERFÜGBAR</b>

<pre>📍 Objekt:        {listing.get('title', 'Nicht verfügbar')}

📌 Adresse:       {listing.get('address', 'Nicht verfügbar')}

💰 Preis:         {listing.get('price', 'Nicht verfügbar')} (entfernt)

🏠 Details:       {listing.get('rooms', 'Nicht verfügbar')} Zimmer

⏰ Verfügbar seit: {first_seen_formatted}</pre>"""
        return self._send_message(message)
    
    def send_price_update(self, update):
        price_trend = "📈" if update.get('old_price', '').replace('€', '').replace('.', '').replace(',', '').replace(' ', '') < update.get('new_price', '').replace('€', '').replace('.', '').replace(',', '').replace(' ', '') else "📉"
        
        message = f"""💰 <b>PREISÄNDERUNG!</b> {price_trend}

<pre>📍 Objekt:        {update['listing'].get('title', 'Nicht verfügbar')}

📌 Adresse:       {update['listing'].get('address', 'Nicht verfügbar')}

💰 Alter Preis:   {update.get('old_price', 'Nicht verfügbar')}

💰 Neuer Preis:   {update.get('new_price', 'Nicht verfügbar')}</pre>

🔗 <b><a href="{update['listing'].get('url', '#')}">» Jetzt ansehen «</a></b>"""
        return self._send_message(message)
    
    def _send_message(self, message):
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(f"{self.api_url}/sendMessage", json=payload)
        return response.json()