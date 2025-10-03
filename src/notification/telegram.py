# src/notification/telegram.py
import requests
import os
from typing import Optional


class TelegramNotifier:
    """Simple Telegram notifications"""
    
    def __init__(self, bot_token: Optional[str] = None, chat_id: Optional[str] = None):
        self.bot_token = bot_token or os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = chat_id or os.getenv('TELEGRAM_CHANNEL_ID')
        
        if not self.bot_token or not self.chat_id:
            print("⚠️  Telegram not configured - notifications disabled")
            self.enabled = False
        else:
            self.enabled = True
            self.api_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    def send_new_property(self, prop) -> bool:
        """Send new property notification"""
        if not self.enabled:
            return False
        
        wbs = "✅ Ja" if prop.wbs_required else "❌ Nein" if prop.wbs_required is False else "❓ N/A"
        source_text = f"🏢 {prop.source.title()}" if prop.source else ""
        
        message = f"""🆕 <b>NEUE WOHNUNG!</b>

<pre>📍 {prop.title[:60]}

📌 {prop.address}

💰 {prop.price}€

🏠 {prop.rooms} Zimmer • {prop.size}m²

🎫 WBS: {wbs}

{source_text}</pre>

🔗 <a href="{prop.url}">Zur Anzeige</a>"""
        
        return self._send(message)
    
    def send_price_update(self, update) -> bool:
        """Send price update notification"""
        if not self.enabled:
            return False
        
        prop = update['property']
        old_price = update['old_price']
        new_price = update['new_price']
        
        trend = "📈" if new_price > old_price else "📉"
        change = abs(((new_price - old_price) / old_price) * 100)
        
        message = f"""💰 <b>PREISÄNDERUNG!</b> {trend}

<pre>📍 {prop.title[:60]}

📌 {prop.address}

💰 Alt: {old_price}€
💰 Neu: {new_price}€

📊 {change:.1f}% {trend}</pre>

🔗 <a href="{prop.url}">Zur Anzeige</a>"""
        
        return self._send(message)
    
    def send_removed_property(self, prop) -> bool:
        """Send removed property notification"""
        if not self.enabled:
            return False
        
        message = f"""❌ <b>NICHT MEHR VERFÜGBAR</b>

<pre>📍 {prop.title[:60]}

📌 {prop.address}

💰 {prop.price}€</pre>"""
        
        return self._send(message)
    
    def _send(self, message: str) -> bool:
        """Send message to Telegram"""
        try:
            response = requests.post(
                f"{self.api_url}/sendMessage",
                json={
                    "chat_id": self.chat_id,
                    "text": message,
                    "parse_mode": "HTML"
                },
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Telegram error: {e}")
            return False