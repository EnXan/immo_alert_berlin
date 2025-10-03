import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime
from database.models import StoredProperty, Property


class PropertyDatabase:
    """Simple JSON file database"""
    
    def __init__(self, db_path: str = "database/database.json"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True, parents=True)
    
    def load(self) -> Dict[str, StoredProperty]:
        """Load properties from file"""
        if not self.db_path.exists():
            return {}
        
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return {
                url: StoredProperty(**prop_data)
                for url, prop_data in data.items()
            }
        except Exception as e:
            print(f"❌ Failed to load database: {e}")
            return {}
    
    def save(self, properties: Dict[str, StoredProperty]) -> None:
        """Save properties to file"""
        try:
            data = {url: prop.to_dict() for url, prop in properties.items()}
            
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Failed to save database: {e}")
    
    def sync(self, current_properties: List[Property]) -> Dict:
        """
        Sync current properties with database
        Returns dict with new, removed, and updated properties
        """
        print(f"📊 Syncing {len(current_properties)} properties...")
        
        stored = self.load()
        current_urls = {p.url for p in current_properties if p.url}
        
        new_properties = []
        updated_properties = []
        removed_properties = []
        
        # Process current properties
        for prop in current_properties:
            if not prop.url:
                continue
                
            if prop.url not in stored:
                # New property
                new_prop = StoredProperty.from_property(prop)
                stored[prop.url] = new_prop
                new_properties.append(new_prop)
                print(f"  🆕 New: {prop.title[:50]}")
            else:
                # Update existing
                existing = stored[prop.url]
                old_price = existing.price
                
                existing.title = prop.title
                existing.address = prop.address
                existing.rooms = prop.rooms
                existing.size = prop.size
                existing.wbs_required = prop.wbs_required
                existing.last_seen = datetime.now().isoformat()
                
                if old_price != prop.price:
                    existing.price = prop.price
                    updated_properties.append({
                        'property': existing,
                        'old_price': old_price,
                        'new_price': prop.price
                    })
                    print(f"  💰 Price changed: {prop.title[:50]} ({old_price}€ → {prop.price}€)")
        
        # Find removed properties
        for url, stored_prop in list(stored.items()):
            if url not in current_urls and stored_prop.status == "active":
                stored_prop.status = "removed"
                stored_prop.last_seen = datetime.now().isoformat()
                removed_properties.append(stored_prop)
                print(f"  ❌ Removed: {stored_prop.title[:50]}")
        
        # Save changes
        self.save(stored)
        
        print(f"✅ Sync complete: {len(new_properties)} new, {len(updated_properties)} updated, {len(removed_properties)} removed")
        
        return {
            'new': new_properties,
            'updated': updated_properties,
            'removed': removed_properties,
            'total_active': len(current_urls)
        }
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        stored = self.load()
        active = [p for p in stored.values() if p.status == "active"]
        
        sources = {}
        for prop in active:
            if prop.source:
                sources[prop.source] = sources.get(prop.source, 0) + 1
        
        return {
            'total': len(stored),
            'active': len(active),
            'removed': len([p for p in stored.values() if p.status == "removed"]),
            'by_source': sources
        }