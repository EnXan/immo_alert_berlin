import json
from datetime import datetime
from pathlib import Path

class ListingDatabase:
    def __init__(self):
        self.db_path = Path("database/database.json")
        self.db_path.parent.mkdir(exist_ok=True)
        self.listings = self._load_db()

    def _load_db(self):
        if self.db_path.exists():
            try:
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        return json.loads(content)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        return {}

    def _save(self):
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.listings, f, indent=2, ensure_ascii=False)
    
    def sync_listings(self, current_listings):
        """
        Synchronisiert die Datenbank mit aktuellen Listings
        - Findet neue Listings
        - Entfernt nicht mehr vorhandene
        - Aktualisiert bestehende
        """
        new_listings = []
        removed_listings = []
        updated_listings = []
        
        # Erstelle Set mit aktuellen IDs
        current_ids = set()
        current_dict = {}
        
        for listing in current_listings:
            listing_id = listing.get('url', f"{listing['title']}_{listing['address']}")
            current_ids.add(listing_id)
            current_dict[listing_id] = listing
        
        # Finde neue und aktualisierte Listings
        for listing_id, listing in current_dict.items():
            if listing_id not in self.listings:
                # Neues Listing
                self.listings[listing_id] = {
                    **listing,
                    'first_seen': datetime.now().isoformat(),
                    'last_seen': datetime.now().isoformat(),
                    'status': 'active'
                }
                new_listings.append(listing)
            else:
                # Bestehendes Listing - aktualisiere last_seen
                self.listings[listing_id]['last_seen'] = datetime.now().isoformat()
                
                # Prüfe ob sich was geändert hat (z.B. Preis)
                old_price = self.listings[listing_id].get('price')
                new_price = listing.get('price')
                
                if old_price != new_price:
                    self.listings[listing_id].update(listing)
                    self.listings[listing_id]['price_history'] = self.listings[listing_id].get('price_history', [])
                    self.listings[listing_id]['price_history'].append({
                        'price': old_price,
                        'changed_at': datetime.now().isoformat()
                    })
                    updated_listings.append({
                        'listing': listing,
                        'old_price': old_price,
                        'new_price': new_price
                    })
        
        # Finde entfernte Listings
        for listing_id in list(self.listings.keys()):
            if listing_id not in current_ids:
                # Listing nicht mehr vorhanden
                removed_listing = self.listings[listing_id].copy()
                removed_listing['removed_at'] = datetime.now().isoformat()
                removed_listings.append(removed_listing)
                
                # Entferne aus aktiver DB
                del self.listings[listing_id]
        
        self._save()
        
        return {
            'new': new_listings,
            'removed': removed_listings,
            'updated': updated_listings,
            'total_active': len(self.listings)
        }
    