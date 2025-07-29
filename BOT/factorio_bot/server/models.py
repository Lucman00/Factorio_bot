from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from ..constants import StatusEmoji

@dataclass
class ServerStatus:
    """Current server state representation"""
    online: bool
    world_name: str
    players: List[str]
    last_updated: datetime
    uptime: Optional[float] = None  # in seconds
    
    @property
    def status_emoji(self) -> str:
        return StatusEmoji.ONLINE.value if self.online else StatusEmoji.OFFLINE.value
    
    @property
    def player_count(self) -> int:
        return len(self.players)