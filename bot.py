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
from EnvyGames.start_server import ServerStarter
from EnvyGames.stop_server import ServerStopper
from discord.errors import LoginFailure, ConnectionClosed, HTTPException
import ssl
import asyncio
import sys

config_manager = ConfigManager('config.json')
log_manager = LogManager()

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        # Do not log or capture KeyboardInterrupt.
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    log_manager.exception("Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix=config_manager.get('bot_setup', 'prefix'), intents=intents)

def log_asyncio_exceptions(loop, context):
    exception = context.get("exception")
    message = context.get("message")

    if exception:
        log_manager.error(f"Caught asyncio exception: {exception}, Message: {message}")
    else:
        log_manager.error(f"Asyncio context error: {message}")

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

    # Set up custom asyncio exception handler for the bot's event loop
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(log_asyncio_exceptions)

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
    if interaction.type == discord.InteractionType.component:
        try:
            custom_id = interaction.data["custom_id"]
            server_index = int(custom_id.split('_')[1])
            await interaction.response.defer(ephemeral=True)

            if custom_id.startswith("start_"):
                response_message, log_message = await process_start_server(server_index)
                await interaction.followup.send(response_message, ephemeral=True)
                log_manager.info(log_message)
            elif custom_id.startswith("stop_"):
                # Proceed with shutdown process but only acknowledge the interaction
                await process_stop_server(server_index, bot, interaction.user.id)
                await interaction.followup.send("Shutdown process initiated.", ephemeral=True)
        except Exception as e:
            error_message = f"Error processing interaction: {e}"
            log_manager.error(error_message)
            await interaction.followup.send("There was an error processing your request.", ephemeral=True)

async def process_start_server(server_index):
    """Process the start server action and return response and log messages."""
    servers = config_manager.get('server_control', 'servers')
    if server_index < len(servers):
        server_info = servers[server_index]
        starter = ServerStarter(server_info, log_manager)
        starter.start_server()
        response_message = f"Starting Server {server_index + 1}"
        log_message = f"Starting Server {server_index + 1}."
        return response_message, log_message
    else:
        log_manager.error(f"Server configuration not found for index {server_index}.")
        return "Server configuration not found.", f"Server configuration not found for index {server_index}."

async def process_stop_server(server_index, bot, user_id):  # Add user_id as an argument
    servers = config_manager.get('server_control', 'servers')
    if server_index < len(servers):
        server_info = servers[server_index]
        # Pass the user_id to ServerStopper
        stopper = ServerStopper(server_info, log_manager, bot, user_id)
        shutdown_successful = await stopper.stop_server()
        if shutdown_successful:
            return True, "Shutdown completed for Server."
        else:
            return False, "Shutdown failed for Server."
    else:
        log_manager.error(f"Server configuration not found for index {server_index}.")
        return False, "Server configuration not found for index."

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

try:
    bot.run(config_manager.get('bot_setup', 'token'))
except LoginFailure:
    log_manager.exception("Authentication failed. Check your bot token.")
except ConnectionClosed as e:
    log_manager.exception("Connection to Discord was closed: %s", e)
except HTTPException as e:
    log_manager.exception("HTTP request to Discord failed: %s", e)
except asyncio.TimeoutError as e:
    log_manager.exception("A timeout occurred while connecting to Discord: %s", e)
except ssl.SSLCertVerificationError as e:
    log_manager.exception("SSL Certificate verification failed: %s", e)
except Exception as e:  # Catch-all for any other exceptions
    log_manager.exception("Failed to start the bot due to an unhandled exception: %s", e)
    raise

