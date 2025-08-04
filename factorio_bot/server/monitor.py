from typing import Tuple
from datetime import datetime
from ..config import Config
from ..R_con import RCONClient, RCONCommands
from .models import ServerStatus
from ..exceptions import RCONError
import logging

logger = logging.getLogger(__name__)

class ServerMonitor:
    """Handles server status checks and health monitoring"""
    
    @staticmethod
    def get_world_name() -> str:
        """Get the current world name from config"""
        return Config.CURRENT_WORLD_NAME or "Unknown World"

    @staticmethod
    def get_status() -> ServerStatus:
        """
        Fetch current server status via RCON
        Returns: ServerStatus object with current state
        """
        try:
            # Get basic info
            players_raw = RCONClient.send(RCONCommands.players())
            
            # Parse player list
            players = [
                line.strip() 
                for line in players_raw.split('\n') 
                if line.strip() and not line.startswith('---')
            ] if players_raw else []
            
            return ServerStatus(
                online=True,
                world_name=ServerMonitor.get_world_name(),  # Use our simplified method
                players=players,
                last_updated=datetime.now()
            )
            
        except RCONError:
            return ServerStatus(
                online=False,
                world_name="Server Offline",
                players=[],
                last_updated=datetime.now()
            )