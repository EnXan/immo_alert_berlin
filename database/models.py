from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class Property:
    """Property from crawler"""
    title: str
    url: Optional[str]
    address: str
    price: float
    rooms: float
    size: float
    wbs_required: Optional[bool] = None
    source: Optional[str] = None


@dataclass
class StoredProperty:
    """Property with metadata"""
    title: str
    url: Optional[str]
    address: str
    price: float
    rooms: float
    size: float
    wbs_required: Optional[bool]
    source: Optional[str]
    first_seen: str
    last_seen: str
    status: str = "active"
    
    @classmethod
    def from_property(cls, prop: Property) -> 'StoredProperty':
        now = datetime.now().isoformat()
        return cls(
            title=prop.title,
            url=prop.url,
            address=prop.address,
            price=prop.price,
            rooms=prop.rooms,
            size=prop.size,
            wbs_required=prop.wbs_required,
            source=prop.source,
            first_seen=now,
            last_seen=now,
            status="active"
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)