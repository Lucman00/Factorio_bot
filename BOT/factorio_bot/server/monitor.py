from typing import Tuple
from datetime import datetime
import time
from ..R_con import RCONClient, RCONCommands
from .models import ServerStatus
from ..exceptions import RCONError

class ServerMonitor:
    """Handles server status checks and health monitoring"""
    
    @staticmethod
    def get_status() -> ServerStatus:
        """
        Fetch current server status via RCON
        Returns: ServerStatus object with current state
        """
        try:
            # Get basic info
            world_name = RCONClient.send(RCONCommands.server_info())
            players_raw = RCONClient.send(RCONCommands.players())
            
            # Parse player list
            players = [
                line.strip() 
                for line in players_raw.split('\n') 
                if line.strip() and not line.startswith('---')
            ] if players_raw else []
            
            return ServerStatus(
                online=True,
                world_name=world_name or "Unknown World",
                players=players,
                last_updated=datetime.now()
            )
            
        except RCONError:
            return ServerStatus(
                online=False,
                world_name="Offline",
                players=[],
                last_updated=datetime.now()
            )
    
    @staticmethod
    def is_online() -> bool:
        """Quick health check"""
        try:
            RCONClient.send(RCONCommands.players(), timeout=2)
            return True
        except RCONError:
            return False