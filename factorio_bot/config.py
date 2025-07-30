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
    RCON_PORT: int = int(os.getenv("RCON_PORT", "27015"))
    RCON_PASSWORD: str = os.getenv("RCON_PASSWORD", "password")
    
    # Bot Settings
    COMMAND_PREFIX: str = os.getenv("COMMAND_PREFIX", "!")
    STATUS_UPDATE_INTERVAL: int = int(os.getenv("STATUS_UPDATE_INTERVAL", "25"))
    
    # Paths (with validation)
    SERVER_PATH: Path = Path(os.getenv("SERVER_PATH", ".")).absolute()
    SERVER_BAT: Path = SERVER_PATH / "server.bat"
    SAVE_GAMES_DIR: Path = (SERVER_PATH / os.getenv("SAVE_GAMES_DIR", "saves")).absolute()


    @classmethod
    def validate(cls):
        """Strict configuration validation"""
        if not cls.TOKEN:
            raise ValueError("DISCORD_TOKEN must be set")
        
        if not cls.CHANNEL_ID:
            raise ValueError("DISCORD_CHANNEL_ID must be set")
        
        if not cls.SERVER_PATH.exists():
            raise ValueError(f"Server path not found: {cls.SERVER_PATH}")
            
        if not cls.SERVER_BAT.exists():
            raise ValueError(f"server.bat not found at {cls.SERVER_BAT}")
        
        cls.SAVE_GAMES_DIR.mkdir(exist_ok=True)

    PANEL_MESSAGE_ID: Optional[int] = None