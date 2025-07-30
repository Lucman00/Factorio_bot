from typing import Dict, Literal
from enum import Enum

class RCONCommands:
    """Predefined RCON commands for Factorio"""
    
    @staticmethod
    def save(filename: str = None) -> str:
        """Trigger a server save"""
        return f"/save{' ' + filename if filename else ''}"
    
    @staticmethod
    def stop() -> str:
        """Graceful server shutdown"""
        return "/quit"
    
    @staticmethod
    def players() -> str:
        """List connected players"""
        return "/players"
    
    @staticmethod
    def server_info() -> str:
        """Get server metadata"""
        return "/silent-command rcon.print(game.name)"  # Returns world name
    
    @staticmethod
    def message(msg: str) -> str:
        """Broadcast message to all players"""
        return f'/silent-command game.print("{msg}")'
    
    @staticmethod
    def ban_player(username: str, reason: str = "") -> str:
        """Ban a player"""
        return f'/ban {username} {reason}'