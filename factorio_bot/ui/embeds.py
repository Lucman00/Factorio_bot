import discord
from datetime import datetime
from typing import Optional
from ..server.models import ServerStatus
from ..constants import StatusEmoji

def generate_status_embed(status: ServerStatus) -> discord.Embed:
    """
    Generate a Discord embed showing server status
    :param status: Current ServerStatus object
    :return: Formatted discord.Embed
    """
    embed = discord.Embed(
        title="Factorio Server Control Panel",
        timestamp=status.last_updated,
        color=discord.Color.green() if status.online else discord.Color.red()
    )
    
    # Status field
    embed.add_field(
        name="Status",
        value=f"{status.status_emoji} {'Online' if status.online else 'Offline'}",
        inline=True
    )
    
    # World info
    embed.add_field(
        name="World",
        value=status.world_name,
        inline=True
    )
    
    # Players field
    player_list = "\n".join(status.players) if status.players else "No players connected"
    embed.add_field(
        name=f"Players ({status.player_count})",
        value=f"```{player_list}```",
        inline=False
    )
    
    # Footer with timestamp
    embed.set_footer(text="Last updated")
    
    return embed