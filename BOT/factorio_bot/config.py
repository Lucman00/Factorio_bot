import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
load_dotenv()

class Config:
    # Discord
    TOKEN: str = os.getenv("DISCORD_TOKEN")
    CHANNEL_ID: int = int(os.getenv("DISCORD_CHANNEL_ID", "0"))
    
    # RCON
    RCON_HOST: str = os.getenv("RCON_HOST", "127.0.0.1")
    RCON_PORT: int = int(os.getenv("RCON_PORT", "5002"))
    RCON_PASSWORD: str = os.getenv("RCON_PASSWORD", "password")
    
    # Bot Settings
    COMMAND_PREFIX: str = os.getenv("COMMAND_PREFIX", "!")
    STATUS_UPDATE_INTERVAL: int = int(os.getenv("STATUS_UPDATE_INTERVAL", "25"))  # Added this line
    
    # Paths
    SAVE_GAMES_DIR: Path = Path(os.getenv("SAVE_GAMES_DIR", "./saves"))
    
    @classmethod
    def validate(cls):
        if not cls.TOKEN:
            raise ValueError("DISCORD_TOKEN must be set")
        if not cls.CHANNEL_ID:
            raise ValueError("DISCORD_CHANNEL_ID must be set")
        cls.SAVE_GAMES_DIR.mkdir(exist_ok=True)
    PANEL_MESSAGE_ID: Optional[int] = None