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

class FactorioBot(commands.Bot):
    """
    Main bot class for Factorio server management
    Handles all Discord interactions and server control
    """
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        self.status_message_id = None 
        
        super().__init__(
            command_prefix=Config.COMMAND_PREFIX,
            intents=intents,
            help_command=None
        )
        
        self.status_updater: Optional[StatusUpdater] = None
        self.status_message: Optional[discord.Message] = None
        
        # Verify configuration on startup
        Config.validate()
        
        # Register events and commands
        self._register_events()
        self._register_commands()
        self.panel_lock = asyncio.Lock()
    
    def _register_events(self) -> None:
        """Register all Discord event listeners"""
        self.event(self.on_ready)
        self.event(self.on_interaction)
    
    def _register_commands(self) -> None:
        """Register all text commands with proper parameters"""
        @self.command(name='status')
        async def status(ctx: commands.Context):
            """Manual status check command"""
            status = ServerMonitor.get_status()
            await ctx.send(embed=generate_status_embed(status))

        @self.command(name='save')
        @requires_admin()
        @handle_errors()
        async def save(ctx: commands.Context, filename: str = None):
            """Manual save command"""
            result = ServerController.save_game(filename)
            await ctx.send(f"💾 {result or 'Game saved successfully!'}")

        @self.command(name='players')
        async def players(ctx: commands.Context):
            """List players command"""
            players = RCONClient.send(RCONCommands.players())
            await ctx.send(f"**Online Players:**\n```{players or 'No players connected'}```")

        @self.command(name='restart')
        @requires_admin()
        @handle_errors()
        async def restart(ctx: commands.Context):
            """Restart server command"""
            await ctx.send("🔄 Restarting server...")
            ServerController.stop_server()
            await asyncio.sleep(5)  # Brief cooldown
            ServerController.start_server()
            await ctx.send("✅ Server restart initiated")
    
    async def on_ready(self) -> None:
        """Called when bot connects to Discord"""

        from .utils.persistence import load_state
        
        logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
        logger.info(f'RCON configured for {Config.RCON_HOST}:{Config.RCON_PORT}')
         
        # Load saved panel ID
        load_state() 

        # Create initial status message if none exists
        await self._ensure_single_panel()
        
        # Initialize status updater
        self.status_updater = StatusUpdater(self)
        


    async def _ensure_single_panel(self):
        """Guarantee exactly one control panel exists"""
        async with self.panel_lock:  # Prevent multiple concurrent runs
            channel = self.get_channel(Config.CHANNEL_ID)
            if not channel:
                raise FactorioBotError("Invalid channel ID")

            # Try to find our existing panel
            if Config.PANEL_MESSAGE_ID:
                try:
                    self.status_message = await channel.fetch_message(Config.PANEL_MESSAGE_ID)
                    return  # Found it, we're done!
                except discord.NotFound:
                    pass  # Message was deleted, continue to create new one

            # Delete ALL other bot messages in the channel
            async for message in channel.history(limit=200):
                if message.author == self.user and message.embeds:
                    try:
                        await message.delete()
                    except discord.NotFound:
                        continue

            # Create exactly one new panel
            status = ServerMonitor.get_status()
            self.status_message = await channel.send(
                embed=generate_status_embed(status),
                view=ServerControlView()
            )
            Config.PANEL_MESSAGE_ID = self.status_message.id
        """Guarantee exactly one control panel exists"""
        channel = self.get_channel(Config.CHANNEL_ID)
        if not channel:
            raise FactorioBotError("Invalid channel ID configured")

        # Delete ALL existing bot panels first
        async for message in channel.history(limit=100):
            if message.author == self.user and message.embeds:
                try:
                    await message.delete()
                except discord.NotFound:
                    continue

        # Create exactly one new panel
        status = ServerMonitor.get_status()
        self.status_message = await channel.send(
            embed=generate_status_embed(status),
            view=ServerControlView()
        )
        self.status_message_id = self.status_message.id
    
    async def on_interaction(self, interaction: discord.Interaction) -> None:
        """Handle all interactions (like button clicks)"""
        if interaction.type == discord.InteractionType.component:
            # Let the view handle the interaction
            await self.process_view_interaction(interaction)
    
    async def process_view_interaction(self, interaction: discord.Interaction) -> None:
        """Process interactions from our control view"""
        try:
            # This will be handled by the view's interaction_check
            await interaction.response.defer(ephemeral=True)
        except discord.NotFound:
            logger.warning(f"Interaction not found: {interaction.id}")
    
    # Command implementations
    @handle_errors()
    async def status_command(self, ctx: commands.Context) -> None:
        """Manual status check command"""
        status = ServerMonitor.get_status()
        await ctx.send(embed=generate_status_embed(status))
    
    @requires_admin()
    @handle_errors()
    async def save_command(self, ctx: commands.Context, filename: Optional[str] = None) -> None:
        """Manual save command"""
        result = ServerController.save_game(filename)
        await ctx.send(f"💾 {result or 'Game saved successfully!'}")
    
    @handle_errors()
    async def players_command(self, ctx: commands.Context) -> None:
        """List players command"""
        players = RCONClient.send(RCONCommands.players())
        await ctx.send(f"**Online Players:**\n```{players or 'No players connected'}```")
    
    @requires_admin()
    @handle_errors()
    async def restart_command(self, ctx: commands.Context) -> None:
        """Restart server command"""
        await ctx.send("🔄 Restarting server...")
        ServerController.stop_server()
        await asyncio.sleep(5)  # Brief cooldown
        ServerController.start_server()
        await ctx.send("✅ Server restart initiated")
    
    async def close(self) -> None:
        """Cleanup on bot shutdown"""
        logger.info("Shutting down bot...")
        
        if self.status_updater:
            self.status_updater.stop()
        
        if self.status_message:
            try:
                await self.status_message.edit(view=None)  # Remove buttons on shutdown
            except discord.NotFound:
                pass
        
        await super().close()

def run_bot():
    """Entry point for running the bot"""
    try:
        bot = FactorioBot()
        bot.run(Config.TOKEN)
    except Exception as e:
        logger.critical(f"Bot crashed: {str(e)}", exc_info=True)
        raise