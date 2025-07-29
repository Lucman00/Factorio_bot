from pathlib import Path
from typing import List, Optional
from ..config import Config
from ..exceptions import FactorioBotError

def validate_save_file(filename: str) -> Path:
    """
    Validate a save file exists and return its full path
    :raises FactorioBotError: If file is invalid
    """
    save_path = Config.SAVE_GAMES_DIR / filename
    
    if not save_path.exists():
        raise FactorioBotError(f"Save file not found: {filename}")
    if not save_path.suffix == '.zip':
        raise FactorioBotError("Save files must be .zip format")
    
    return save_path

def list_save_files() -> List[str]:
    """List all valid save files in the saves directory"""
    return [
        f.name for f in Config.SAVE_GAMES_DIR.glob('*.zip') 
        if f.is_file()
    ]

def get_latest_save() -> Optional[Path]:
    """Get the most recently modified save file"""
    saves = list(Config.SAVE_GAMES_DIR.glob('*.zip'))
    if not saves:
        return None
    return max(saves, key=lambda f: f.stat().st_mtime)