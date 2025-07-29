import json
from pathlib import Path
from ..config import Config

CONFIG_FILE = Path('bot_state.json')

def save_state():
    """Save persistent state to file"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump({'panel_message_id': Config.PANEL_MESSAGE_ID}, f)

def load_state():
    """Load persistent state from file"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            data = json.load(f)
            Config.PANEL_MESSAGE_ID = data.get('panel_message_id')