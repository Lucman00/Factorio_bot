from discord.ext import commands, tasks
from typing import Optional
import discord
import logging
from ..server.monitor import ServerMonitor
from ..ui.embeds import generate_status_embed
from ..config import Config
from ..exceptions import RCONError

logger = logging.getLogger(__name__)

class StatusUpdater:
    """Handles periodic status updates"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.update_status.start()

    @tasks.loop(seconds=Config.STATUS_UPDATE_INTERVAL)
    async def update_status(self):
        """Update the existing panel only"""
        if not self.bot.status_message:
            return
            
        try:
            status = ServerMonitor.get_status()
            await self.bot.status_message.edit(
                embed=generate_status_embed(status)
            )
        except discord.NotFound:
            self.bot.status_message = None
        except Exception as e:
            logger.error(f"Update failed: {e}")

    @update_status.before_loop
    async def before_update_status(self):
        await self.bot.wait_until_ready()

    def stop(self):
        self.update_status.cancel()