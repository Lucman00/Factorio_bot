import discord
from discord.ui import Button, View
from ..constants import ButtonIDs
from ..server.controller import ServerController
from ..exceptions import ServerControlError

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

    async def _handle_start(self, interaction: discord.Interaction) -> None:
        """Start server button handler"""
        await interaction.response.defer(ephemeral=True, thinking=True)
        ServerController.start_server()
        await interaction.followup.send("🚀 Server starting... This may take a minute.")

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