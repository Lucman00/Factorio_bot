import subprocess
import platform
from pathlib import Path
from ..config import Config
from ..R_con import RCONClient, RCONCommands
from ..exceptions import ServerControlError

class ServerController:
    @staticmethod
    def start_server(save_file: Path) -> bool:
        try:
            factorio = Config.get_factorio_binary()

            cmd = [
                str(Config.get_factorio_binary()),
                "--start-server", str(save_file),
                "--rcon-port", str(Config.RCON_PORT),
                "--rcon-password", Config.RCON_PASSWORD,
                "--port", str(Config.GAME_PORT)
            ]


            kwargs = {}
            if platform.system() == "Windows":
                kwargs.update({
                    'creationflags': subprocess.CREATE_NEW_PROCESS_GROUP,
                    'shell' : True
                    })

            subprocess.Popen(cmd, **kwargs)
            
            return True
        except Exception as e:
            raise ServerControlError(f"Start failed:{e}") from e
        
    @staticmethod
    def stop_server() -> bool:
        """Graceful server shutdown"""
        try:
            RCONClient.send(RCONCommands.save())
            RCONClient.send(RCONCommands.stop())
            Config.CURRENT_WORLD_NAME = None
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