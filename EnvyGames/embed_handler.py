import discord
import json
from core.logging.logger import LogManager
from core.config_manager import ConfigManager
from EnvyGames.create_embed import generate_server_embed

log_manager = LogManager()
config_manager = ConfigManager('config.json')

async def handle_embed_posting(bot):
    embed_config = config_manager.get('embed_setup')
    channel = bot.get_channel(int(embed_config['embed_channel_id']))

    # Handling the existing embed message
    try:
        with open('core/embed_message_id.json', 'r') as file:
            message_data = json.load(file)
            message_id = message_data.get('message_id')

        if message_id:
            await channel.fetch_message(int(message_id))
            log_manager.info("Existing embed message found.")
            return

    except (FileNotFoundError, discord.NotFound, json.JSONDecodeError):
        log_manager.info("Existing embed message not found. Posting new embed.")

    if channel:
        embed = generate_server_embed(embed_config)
        message = await channel.send(embed=embed)
        save_embed_message_id(message.id)  # Save the new message ID
    else:
        log_manager.error("Embed channel not found.")

def save_embed_message_id(message_id):
    with open('core/embed_message_id.json', 'w') as file:
        json.dump({'message_id': message_id}, file)
