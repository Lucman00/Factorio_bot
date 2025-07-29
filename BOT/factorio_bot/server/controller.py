import subprocess
from pathlib import Path
from ..config import Config
from ..R_con import RCONClient, RCONCommands
from ..exceptions import ServerControlError

class ServerController:
    """Handles server start/stop operations"""
    
    @staticmethod
    def start_server(save_file: str = None) -> bool:
        """
        Launch the Factorio server
        :param save_file: Optional save file to load
        :return: True if successful
        :raises ServerControlError: If startup fails
        """
        try:
            cmd = [
                "factorio",
                "--start-server",
                save_file or Config.SAVE_GAMES_DIR / "latest.zip",
                "--rcon-port", str(Config.RCON_PORT),
                "--rcon-password", Config.RCON_PASSWORD
            ]
            
            # Start in new process group
            subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True
            )
            return True
            
        except Exception as e:
            raise ServerControlError(f"Failed to start server: {e}") from e
    
    @staticmethod
    def stop_server() -> bool:
        """Graceful server shutdown"""
        try:
            RCONClient.send(RCONCommands.save())
            RCONClient.send(RCONCommands.stop())
            return True
        except Exception as e:
            raise ServerControlError(f"Failed to stop server: {e}") from e
    
    @staticmethod
    def save_game(filename: str = None) -> str:
        """Trigger a manual save"""
        try:
            return RCONClient.send(RCONCommands.save(filename))
        except Exception as e:
            raise ServerControlError(f"Save failed: {e}") from e