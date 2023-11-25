import discord
from .logging.logger import LogManager

log_manager = LogManager()

async def handle_general_error(error):
    if isinstance(error, discord.HTTPException):
        log_manager.error(f'HTTPException: {error}')
        # Handle HTTP exceptions (e.g., network issues, Discord API problems)

    elif isinstance(error, discord.Forbidden):
        log_manager.error(f'Forbidden: You do not have permission to do that: {error}')
        # Handle errors due to forbidden actions (e.g., trying to ban someone without permission)

    elif isinstance(error, discord.NotFound):
        log_manager.error(f'NotFound: Requested resource was not found: {error}')
        # Handle errors where a resource (e.g., a message or user) was not found

    elif isinstance(error, discord.InvalidArgument):
        log_manager.error(f'InvalidArgument: Invalid argument passed: {error}')
        # Handle errors due to invalid arguments provided to a method or API call

    else:
        # Generic error handler for anything else
        log_manager.error(f'General Error: {error}')
