import discord
from discord.ui import View, Select, Button
from typing import Optional
from pathlib import Path
from ..config import Config
from ..server.controller import ServerController
from ..constants import ButtonIDs
from ..utils.logging_utils import logger

class SaveSelectView(View):
    def __init__(self, saves: list[tuple[Path, str]]):
        super().__init__()
        options = [
            discord.SelectOption(
                label=name,
                value=str(i)  # Store index
            ) for i, (_, name) in enumerate(saves)
        ]
        
        self.select = Select(
            placeholder="Choose a save file...",
            options=options[:25]  # Discord limits to 25 options
        )
        self.select.callback = self.on_select
        self.add_item(self.select)
        
        self.selected_save: Optional[Path] = None
        self.selected_save_name: Optional[str] = None
        self.saves = saves

    async def on_select(self, interaction: discord.Interaction):
        selected_index = int(self.select.values[0])
        self.selected_save = self.saves[selected_index][0]
        self.selected_save_name = self.saves[selected_index][1]  # Store display name
        await interaction.response.defer()
        self.stop()


class ServerControlView(View):
    """Persistent server control buttons"""
    
    def __init__(self):
        super().__init__(timeout=None)
        self._setup_buttons()
    
    def _setup_buttons(self) -> None:
        # Start Button
        self.add_item(Button(
            style=discord.ButtonStyle.green,
            label="Start Server",
            emoji="🟢",
            custom_id=ButtonIDs.START_SERVER.value,
            row=0
        ))
        
        # Save Button
        self.add_item(Button(
            style=discord.ButtonStyle.blurple,
            label="Save Game",
            emoji="💾",
            custom_id=ButtonIDs.MANUAL_SAVE.value,
            row=0
        ))
        
        # Stop Button
        self.add_item(Button(
            style=discord.ButtonStyle.red,
            label="Stop Server",
            emoji="🛑",
            custom_id=ButtonIDs.STOP_SERVER.value,
            row=0
        ))
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Global permission check"""
        if not any(role.name == "Factorio" for role in interaction.user.roles):
            await interaction.response.send_message(
                "❌ You don't have permission to control the server.",
                ephemeral=True
            )
            return False
        return True

    async def _handle_interaction(self, interaction: discord.Interaction):
        """Central interaction handler"""
        custom_id = interaction.data.get('custom_id')
        if not custom_id:
            return

        try:
            if custom_id == ButtonIDs.START_SERVER.value:
                await self._handle_start(interaction)
            elif custom_id == ButtonIDs.MANUAL_SAVE.value:
                await self._handle_save(interaction)
            elif custom_id == ButtonIDs.STOP_SERVER.value:
                await self._handle_stop(interaction)
        except Exception as e:
            await interaction.followup.send(
                f"⚠️ Error: {str(e)}",
                ephemeral=True
            )

    async def _handle_start(self, interaction: discord.Interaction):
        saves = Config.get_all_saves()
        if not saves:
            await interaction.response.send_message(
                "❌ No save files found!", 
                ephemeral=True
            )
            return

        view = SaveSelectView(saves)
        await interaction.response.send_message(
            "Select a save file to load:",
            view=view,
            ephemeral=True
        )
        
        # Wait for selection
        await view.wait()
        if view.selected_save:
            Config.CURRENT_WORLD_NAME = view.selected_save_name
            await interaction.followup.send(
                f"🚀 Starting server with {view.selected_save.name}...",
                ephemeral=True
            )
            ServerController.start_server(view.selected_save)


    async def _handle_save(self, interaction: discord.Interaction) -> None:
        """Manual save button handler"""
        await interaction.response.defer(ephemeral=True, thinking=True)
        result = ServerController.save_game()
        await interaction.followup.send(f"💾 {result or 'Game saved successfully!'}")

    async def _handle_stop(self, interaction: discord.Interaction) -> None:
        """Stop server button handler"""
        await interaction.response.defer(ephemeral=True, thinking=True)
        ServerController.stop_server()
        await interaction.followup.send("🛑 Server shutdown initiated.")