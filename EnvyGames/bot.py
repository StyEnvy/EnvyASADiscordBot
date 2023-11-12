import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import has_role
from config import (BOT_TOKEN, COMMAND_PREFIX, STATUS_CHANNEL_ID,
                    ARK_ADMIN_ROLE, BOT_TIMEZONE, GAME_STATUS)
from discord_interface import DiscordInterface
from ark_server_manager import ArkServerManager
from bot_logger import log
from datetime import datetime
import pytz

# Define the intents for the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)
# Instantiate the ArkServerManager.py not to be confused with ASE's ASM.
ark_manager = ArkServerManager()
discord_interface = DiscordInterface(bot, STATUS_CHANNEL_ID)

@bot.event
async def on_ready():
    try:
        log('Bot is ready.', 'INFO')
        await bot.change_presence(activity=discord.Game(name=GAME_STATUS))

        # Check for an existing status message and update or post a new one
        existing_message_id = discord_interface.get_existing_message_id()
        if existing_message_id:
            try:
                # Attempt to update the existing status message
                await discord_interface.update_status_embed("Checking status...")
            except Exception as e:
                log(f'Failed to update existing status message: {e}', 'ERROR')
                # If failed to update, post a new status embed
                await discord_interface.post_status_embed("Initializing...")
        else:
            # If no existing status message found, post a new one
            await discord_interface.post_status_embed("Initializing...")
        # Schedule the status check loop to start
        discord_interface.schedule_status_check(ark_manager)
    except Exception as e:
        log(f'An error occurred during the on_ready event: {e}', 'ERROR')

@bot.command(name='startasa')
@has_role(ARK_ADMIN_ROLE)
async def start_server(ctx):
    user_info = f"{ctx.message.author} (ID: {ctx.message.author.id})"
    if ark_manager.start_server(user_info):
        await ctx.send('Server is starting...')
        # Set the server start time to now
        start_time = datetime.now(pytz.timezone(BOT_TIMEZONE))
        discord_interface.set_server_start_time(start_time)
        # Update the status embed to show the server as online and with the correct start time
        await discord_interface.update_status_embed('Online')
    else:
        await ctx.send('Failed to start the server.')

@bot.command(name='shutdownasa')
@has_role(ARK_ADMIN_ROLE)
async def shutdown_server(ctx):
    await ctx.send('Initiating server shutdown sequence...')
    # Warn players that the server is shutting down
    warning_response = ark_manager.send_rcon_command("serverchat The server is shutting down in 5 minutes. Please log-off the server.")
    log(f'Server chat warning response: {warning_response}', 'INFO')
    await asyncio.sleep(300)  # 300 seconds = 5 minutes
    # Shut down the server
    shutdown_response = ark_manager.shutdown_server()
    await ctx.send(f'Server shutdown command issued. Response: {shutdown_response}') 
    # Update the status embed to show the server as offline
    await discord_interface.update_status_embed('Offline')

@bot.command(name='restartasa')
@has_role(ARK_ADMIN_ROLE)
async def restart_server(ctx):
    user_info = f"{ctx.message.author} (ID: {ctx.message.author.id})"
    response = ark_manager.restart_server(user_info)
    await ctx.send(f'Server restart command issued. Response: {response}')

@bot.event
async def on_error(event, *args, **kwargs):
    log(f'An error occurred during the {event} event.', 'ERROR')

# Start the bot
bot.run(BOT_TOKEN)
