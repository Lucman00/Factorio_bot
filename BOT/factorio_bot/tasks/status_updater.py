from discord.ext import commands, tasks
from typing import Optional
import discord
import logging
from ..server.monitor import ServerMonitor
from ..ui.embeds import generate_status_embed
from ..ui.views import ServerControlView
from ..config import Config
from ..exceptions import RCONError

logger = logging.getLogger(__name__)

class StatusUpdater:
    """Handles periodic server status updates"""
    
    UPDATE_INTERVAL = Config.STATUS_UPDATE_INTERVAL
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.status_message: Optional[discord.Message] = None
        self.update_status.start()
    
    @tasks.loop(seconds=UPDATE_INTERVAL)
    async def update_status(self):
        """Update the existing panel only"""
        if not hasattr(self.bot, 'status_message') or not self.bot.status_message:
            return

        try:
            status = ServerMonitor.get_status()
            embed = generate_status_embed(status)
            await self.bot.status_message.edit(embed=embed)
        except discord.NotFound:
            # Panel was deleted - let bot recreate it on next cycle
            self.bot.status_message = None
        except Exception as e:
            logger.error(f"Status update failed: {e}")
        """Background task to update status message"""
        try:
            status = ServerMonitor.get_status()
            embed = generate_status_embed(status)
            channel = self.bot.get_channel(Config.CHANNEL_ID)
            
            if not channel:
                logger.error(f"Channel ID {Config.CHANNEL_ID} not found")
                return
                
            if self.status_message is None:
                # Create new panel if none exists
                self.status_message = await channel.send(
                    embed=embed,
                    view=ServerControlView()
                )
            else:
                try:
                    # Try to edit existing message
                    await self.status_message.edit(embed=embed)
                except discord.NotFound:
                    # Recreate if message was deleted
                    self.status_message = await channel.send(
                        embed=embed,
                        view=ServerControlView()
                    )
                    
        except RCONError as e:
            logger.error(f"RCON error during status update: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in status updater: {e}", exc_info=True)
    
    @update_status.before_loop
    async def before_update_status(self):
        await self.bot.wait_until_ready()
    
    def stop(self):
        self.update_status.cancel()