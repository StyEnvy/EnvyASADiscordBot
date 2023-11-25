import discord
from discord.ext import commands
from core.config_manager import ConfigManager
from core.logging.logger import LogManager
from core.on_error import handle_general_error
from core.on_command_error import handle_command_error
from EnvyGames.create_embed import generate_server_embed
from core.utils import save_embed_message_id
from EnvyGames.check_server_status import check_server_status
from EnvyGames.update_embed import update_embed
from EnvyGames.server_control_buttons import create_server_control_buttons
from core.bot_utils import save_control_buttons_message_id
from EnvyGames.embed_handler import handle_embed_posting
from EnvyGames.button_handler import handle_server_control_buttons
from EnvyGames.server_control import start_server, stop_server
import asyncio
import json

config_manager = ConfigManager('config.json')
log_manager = LogManager()
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix=config_manager.get('bot_setup', 'prefix'), intents=intents)

async def status_update_loop():
    log_manager.info("Status update loop started.")
    while True:
        log_manager.info("Beginning status update check.")
        embed_config = config_manager.get('embed_setup')
        for server in embed_config['servers']:
            status, player_count = await check_server_status(server)
            # Update server status in your embed
            await update_embed(bot, server['name'], status, player_count, config_manager)
        await asyncio.sleep(embed_config['status_check_interval'])

@bot.event
async def on_ready():
    log_manager.info(f'{bot.user.name} has connected to Discord!')
    await handle_embed_posting(bot)
    await handle_server_control_buttons(bot)

    # Start the status update loop
    bot.loop.create_task(status_update_loop())

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Add your message handling logic here
    await bot.process_commands(message)

@bot.event
async def on_interaction(interaction):
    # Ensure it's a button interaction
    if interaction.type == discord.InteractionType.component:
        try:
            custom_id = interaction.data["custom_id"]
            server_index = int(custom_id.split('_')[1])

            # Defer the response to acknowledge the interaction
            await interaction.response.defer(ephemeral=True)

            if custom_id.startswith("start_"):
                # Process start server interaction
                response_message, log_message = await process_start_server(server_index)
            elif custom_id.startswith("stop_"):
                # Process stop server interaction
                response_message, log_message = await process_stop_server(server_index)

            # Log the result of processing
            log_manager.info(log_message)

            # Send the actual response after processing
            await interaction.followup.send(response_message, ephemeral=True)

        except Exception as e:
            error_message = f"Error processing interaction: {e}"
            log_manager.error(error_message)
            # Send an error message as a follow-up
            await interaction.followup.send("There was an error processing your request.", ephemeral=True)

async def process_start_server(server_index):
    """Process the start server action and return response and log messages."""
    start_server(server_index)
    response_message = f"Starting Server {server_index + 1}"
    log_message = f"Starting Server {server_index + 1}."
    return response_message, log_message

async def process_stop_server(server_index):
    """Process the stop server action and return response and log messages."""
    await stop_server(server_index)
    response_message = f"Stopping Server {server_index + 1}"
    log_message = f"Stopping Server {server_index + 1}."
    return response_message, log_message

# Error Handlers - using external error handler
@bot.event
async def on_command_error(ctx, error):
    await handle_command_error(ctx, error)

# General Error Handler
async def on_error(event_method, *args, **kwargs):
    error = args[0]  # Assuming the error is the first argument
    await handle_general_error(error)

# Attach the general error handler
bot.add_listener(on_error, 'on_error')

# Run the Bot
bot.run(config_manager.get('bot_setup', 'token'))
