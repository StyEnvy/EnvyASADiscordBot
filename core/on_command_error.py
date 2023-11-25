from discord.ext import commands
from .logging.logger import LogManager

log_manager = LogManager()

async def handle_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        log_manager.warning(f'Command not found: {ctx.message.content}')
        await ctx.send('Sorry, I don\'t understand that command.')

    elif isinstance(error, commands.MissingRequiredArgument):
        log_manager.warning(f'Missing argument in command: {ctx.command}')
        await ctx.send(f'Missing required argument for {ctx.command}.')

    elif isinstance(error, commands.CommandOnCooldown):
        log_manager.warning(f'Command on cooldown: {ctx.command}')
        await ctx.send(f'That command is on cooldown. Please wait before using it again.')

    elif isinstance(error, commands.CheckFailure):
        log_manager.warning(f'User lacks permission for command: {ctx.command}')
        await ctx.send('You do not have the required permissions to use this command.')

    else:
        # Log other types of errors
        log_manager.error(f'Error in command: {ctx.message.content}, Error: {error}')
        await ctx.send('An error occurred while executing the command.')
