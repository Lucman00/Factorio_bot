from enum import Enum

class ButtonIDs(Enum):
    START_SERVER = "start_server"
    MANUAL_SAVE = "manual_save"
    STOP_SERVER = "stop_server"

class StatusEmoji(Enum):
    ONLINE = "🟢"
    OFFLINE = "🔴"
    STARTING = "🟡"

RCON_TIMEOUT = 10  # seconds
STATUS_UPDATE_INTERVAL = 25  # seconds