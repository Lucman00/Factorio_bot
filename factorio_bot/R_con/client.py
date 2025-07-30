from rcon.source import Client
from typing import Optional
import asyncio
from ..config import Config
from ..exceptions import RCONError
from ..constants import RCON_TIMEOUT

class RCONClient:
    """Thread-safe RCON client wrapper with error handling"""
    
    @staticmethod
    def send(command: str, timeout: int = RCON_TIMEOUT) -> Optional[str]:
        """
        Execute an RCON command
        :param command: The command to send
        :param timeout: Connection timeout in seconds
        :return: Server response or None if command expects no response
        :raises RCONError: If communication fails
        """
        try:
            with Client(
                Config.RCON_HOST,
                Config.RCON_PORT,
                passwd=Config.RCON_PASSWORD,
                timeout=timeout
            ) as client:
                response = client.run(command)
                return response.strip() if response else None
        except Exception as e:
            raise RCONError(f"RCON command failed: {e}") from e

    @staticmethod
    async def send_async(command: str, timeout: int = RCON_TIMEOUT) -> Optional[str]:
        """Async wrapper for RCON commands"""
        return await asyncio.to_thread(RCONClient.send, command, timeout)