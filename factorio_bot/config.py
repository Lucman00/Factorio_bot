import os
import platform
from datetime import datetime
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
load_dotenv( Path(__file__).parent.parent / ".env")

class Config:
# Discord
    TOKEN: str = os.getenv("DISCORD_TOKEN")
    CHANNEL_ID: int = int(os.getenv("DISCORD_CHANNEL_ID", "0"))
    
    CURRENT_WORLD_NAME: str = None

    # RCON
    RCON_HOST: str = os.getenv("RCON_HOST", "127.0.0.1")
    RCON_PORT: int = int(os.getenv("RCON_PORT", "27015"))
    RCON_PASSWORD: str = os.getenv("RCON_PASSWORD", "password")
    
    # Bot Settings
    COMMAND_PREFIX: str = os.getenv("COMMAND_PREFIX", "!")
    STATUS_UPDATE_INTERVAL: int = int(os.getenv("STATUS_UPDATE_INTERVAL", "25"))

    # Game port (obviously)
    GAME_PORT : int = int(os.getenv("GAME_PORT", "34197"))

    
    # Paths (with validation)
    SERVER_PATH: Path = Path(os.getenv("SERVER_PATH", ".")).absolute()
    SERVER_BAT: Path = SERVER_PATH / "server.bat"
    SAVE_GAMES_DIR: Path = (SERVER_PATH / os.getenv("SAVE_GAMES_DIR", "saves")).absolute()

    @classmethod
    def get_all_saves(cls) -> list[tuple[Path, str]]:
        """Get all saves with formatted display strings"""
        saves = []
        for save in sorted(
            cls.SAVE_GAMES_DIR.glob("*.zip*"),  # Includes .zip.autosave
            key=lambda f: f.stat().st_mtime,
            reverse=True  # Newest first
        ):
            timestamp = datetime.fromtimestamp(save.stat().st_mtime)
            saves.append((
                save,
                f"{save.stem} ({timestamp:%Y-%m-%d %H:%M})"
            ))
        return saves

    @classmethod
    def get_factorio_binary(cls) -> Path:
        if platform.system() == "Windows":
            exe = cls.SERVER_PATH / "bin/x64/factorio.exe"
        else:
            exe = cls.SERVER_PATH / "bin/x64/factorio"

        if not exe.exists():
            raise FileNotFoundError(f"Factorio binary not found at {exe}")
        return exe

    @classmethod
    def validate(cls):
        """Strict configuration validation"""
        if not cls.TOKEN:
            raise ValueError("DISCORD_TOKEN must be set")
        
        if not cls.CHANNEL_ID:
            raise ValueError("DISCORD_CHANNEL_ID must be set")
        
        if not cls.SERVER_PATH.exists():
            raise ValueError(f"Server path not found: {cls.SERVER_PATH}")
            
        
        
        cls.SAVE_GAMES_DIR.mkdir(exist_ok=True)

    PANEL_MESSAGE_ID: Optional[int] = None
