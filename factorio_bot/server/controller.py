import subprocess
from pathlib import Path
from ..config import Config
from ..R_con import RCONClient, RCONCommands
from ..exceptions import ServerControlError

class ServerController:
    """Handles server start/stop operations"""
    
    @staticmethod
    def start_server(save_file: str = None) -> bool:
        try:
            if not Config.SERVER_BAT.exists():
                raise ServerControlError("Server startup file not found")

            # Use the save file or default to latest
            save_path = save_file or Config.SAVE_GAMES_DIR / "latest.zip"
            
            subprocess.Popen(
                [str(Config.SERVER_BAT)],  # Full path to bat file
                cwd=Config.SERVER_PATH,    # Run from server directory
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
            return True
            
        except Exception as e:
            raise ServerControlError(f"Startup failed: {e}") from e

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