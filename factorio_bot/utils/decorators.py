from functools import wraps
import discord
import logging
from discord.ext import commands
from ..exceptions import FactorioBotError

def requires_admin():
    """
    Decorator to restrict commands to admin users
    Usage: @requires_admin()
    """
    def predicate(ctx: commands.Context):
        if not any(role.name == "Factorio Admin" for role in ctx.author.roles):
            raise FactorioBotError("You don't have permission to use this command")
        return True
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            ctx = args[0] if isinstance(args[0], commands.Context) else args[1]
            predicate(ctx)
            return await func(*args, **kwargs)
        return wrapper
    
    return decorator

def handle_errors():
    """
    Decorator to standardize error handling
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except FactorioBotError as e:
                ctx = args[0] if isinstance(args[0], commands.Context) else args[1]
                if isinstance(ctx, discord.Interaction):
                    await ctx.response.send_message(f"⚠️ {str(e)}", ephemeral=True)
                else:
                    await ctx.send(f"⚠️ {str(e)}")
            except Exception as e:
                logger = logging.getLogger('factorio_bot')
                logger.error(f"Unhandled error in {func.__name__}: {str(e)}", exc_info=True)
                # Don't expose internal errors to users
                error_msg = "An unexpected error occurred"
                if isinstance(ctx, discord.Interaction):
                    await ctx.response.send_message(f"⚠️ {error_msg}", ephemeral=True)
                else:
                    await ctx.send(f"⚠️ {error_msg}")
        return wrapper
    return decorator