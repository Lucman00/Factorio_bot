import asyncio
import discord
from discord.ext import commands
from pathlib import Path
from typing import Optional

# Local imports
from .R_con.client import RCONClient
from .R_con.commands import RCONCommands
from .server.monitor import ServerMonitor
from .server.controller import ServerController
from .ui.views import ServerControlView
from .ui.embeds import generate_status_embed
from .tasks.status_updater import StatusUpdater
from .utils.logging_utils import logger
from .utils.decorators import requires_admin, handle_errors
from .config import Config
from .exceptions import FactorioBotError
from .utils.persistence import load_state, save_state

class FactorioBot(commands.Bot):
    """Main bot class for Factorio server management"""
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        
        super().__init__(
            command_prefix=Config.COMMAND_PREFIX,
            intents=intents,
            help_command=None
        )
        
        self.status_updater: Optional[StatusUpdater] = None
        self.status_message: Optional[discord.Message] = None
        self.panel_lock = asyncio.Lock()
        
        # Verify configuration
        Config.validate()
        
        # Register events and commands
        self._register_events()
        self._register_commands()

    def _register_events(self) -> None:
        """Register all Discord event listeners"""
        self.event(self.on_ready)

    async def on_interaction(self, interaction: discord.Interaction):
        """Handle all interactions (like button clicks)"""
        if interaction.type == discord.InteractionType.component:
            # Let the view handle the interaction
            view = ServerControlView()
            await view._handle_interaction(interaction)

    def _register_commands(self) -> None:
        """Register all text commands"""
        @self.command(name='status')
        async def status(ctx: commands.Context):
            """Manual status check"""
            status = ServerMonitor.get_status()
            await ctx.send(embed=generate_status_embed(status))

        @self.command(name='save')
        @requires_admin()
        @handle_errors()
        async def save(ctx: commands.Context, filename: str = None):
            """Manual save"""
            result = ServerController.save_game(filename)
            await ctx.send(f"💾 {result or 'Game saved!'}")

        @self.command(name='players')
        async def players(ctx: commands.Context):
            """List players"""
            players = RCONClient.send(RCONCommands.players())
            await ctx.send(f"**Players:**\n```{players or 'None'}```")

    async def on_ready(self) -> None:
        """Bot startup handler"""
        logger.info(f'Logged in as {self.user}')
        
        # Load persisted state
        load_state()
        
        # Ensure single control panel exists
        await self._ensure_single_panel()
        
        # Start status updater
        self.status_updater = StatusUpdater(self)

    async def _ensure_single_panel(self) -> None:
        """Guarantee exactly one control panel exists"""
        async with self.panel_lock:
            channel = self.get_channel(Config.CHANNEL_ID)
            if not channel:
                raise FactorioBotError("Invalid channel ID")

            # Try to find existing panel
            if Config.PANEL_MESSAGE_ID:
                try:
                    self.status_message = await channel.fetch_message(Config.PANEL_MESSAGE_ID)
                    return
                except discord.NotFound:
                    pass

            # Clean up any existing panels
            async for message in channel.history(limit=100):
                if message.author == self.user and message.embeds:
                    try:
                        await message.delete()
                    except discord.NotFound:
                        continue

            # Create new panel
            status = ServerMonitor.get_status()
            self.status_message = await channel.send(
                embed=generate_status_embed(status),
                view=ServerControlView()
            )
            Config.PANEL_MESSAGE_ID = self.status_message.id
            save_state()

    async def close(self) -> None:
        """Clean shutdown"""
        logger.info("Shutting down...")
        if self.status_updater:
            self.status_updater.stop()
        await super().close()

def run_bot():
    """Bot entry point"""
    try:
        bot = FactorioBot()
        bot.run(Config.TOKEN)
    except Exception as e:
        logger.critical(f"Bot crashed: {e}", exc_info=True)
        raise