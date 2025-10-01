import requests
import os

class TelegramNotifier:
    def __init__(self, channel_id, bot_token=None):
        self.bot_token = bot_token or os.getenv('TELEGRAM_BOT_TOKEN')
        if not self.bot_token:
            raise ValueError("Bot token must be provided either as parameter or via TELEGRAM_BOT_TOKEN environment variable")
        self.chat_id = channel_id
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"

    def send_new_listing(self, listing):
        message = f"""
        🆕 <b>Neue Wohnung gefunden!</b>

        📍 {listing['title']}
        📌 {listing['address']}
        💰 {listing['price']}
        🏠 {listing['rooms']} Zimmer, {listing['size']}
        🎫 WBS: {listing['wbs_required']}

        🔗 <a href="{listing['url']}">Zur Wohnung</a>
        """
        return self._send_message(message)
    
    def send_removed_listing(self, listing):
        message = f"""
        ❌ <b>Wohnung nicht mehr verfügbar</b>

        📍 {listing['title']}
        📌 {listing['address']}
        💰 {listing['price']}
        🏠 {listing['rooms']} Zimmer

        ⏰ War verfügbar seit: {listing.get('first_seen', 'Unknown')}
        """
        return self._send_message(message)
    
    def send_price_update(self, update):
        message = f"""
        💰 <b>Preisänderung!</b>

        📍 {update['listing']['title']}
        📌 {update['listing']['address']}

        Alter Preis: {update['old_price']}
        Neuer Preis: {update['new_price']}

        🔗 <a href="{update['listing']['url']}">Zur Wohnung</a>
        """
        return self._send_message(message)
    
    def send_summary(self, result):
        message = f"""
        📊 <b>Scan-Zusammenfassung</b>

        🆕 Neue: {len(result['new'])}
        ❌ Entfernt: {len(result['removed'])}
        💰 Preisänderungen: {len(result['updated'])}
        📁 Gesamt aktiv: {result['total_active']}
        """
        return self._send_message(message)
    
    def _send_message(self, message):
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(f"{self.api_url}/sendMessage", json=payload)
        return response.json()