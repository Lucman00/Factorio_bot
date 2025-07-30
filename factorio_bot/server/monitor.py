from typing import Tuple
from datetime import datetime
import time
from ..R_con import RCONClient, RCONCommands
from .models import ServerStatus
from ..exceptions import RCONError
import logging

logger = logging.getLogger(__name__)

class ServerMonitor:
    """Handles server status checks and health monitoring"""
    
    @staticmethod
    def get_world_name() -> str:
        """Safely get world name with fallback"""
        try:
            # First try the direct RCON command
            world_name = RCONClient.send(RCONCommands.server_info())
            if world_name and not world_name.startswith("Error"):
                return world_name.strip()
            
            # Fallback to alternative command if first fails
            world_name = RCONClient.send("/silent-command rcon.print(game.connected_players[1].surface.name)")
            return world_name.strip() if world_name else "Unknown World"
            
        except Exception as e:
            logger.warning(f"Failed to get world name: {e}")
            return "Factorio World"  # Default fallback name

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
                world_name=ServerMonitor.get_world_name(),
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