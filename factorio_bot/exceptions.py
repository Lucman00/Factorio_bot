class FactorioBotError(Exception):
    """Base exception for all bot-related errors"""
    pass

class RCONError(FactorioBotError):
    """RCON communication failed"""
    pass

class ServerControlError(FactorioBotError):
    """Server start/stop operation failed"""
    pass