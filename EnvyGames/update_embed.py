import discord
import json
from core.logging.logger import LogManager

log_manager = LogManager()

async def update_embed(bot, server_name, status, player_count, config_manager):
    with open('core/embed_message_id.json', 'r') as file:
        message_data = json.load(file)
    message_id = message_data.get('message_id')

    if not message_id:
        log_manager.error("Embed message ID not found.")
        return

    channel_id = config_manager.get('embed_setup', 'embed_channel_id')
    channel = bot.get_channel(int(channel_id))
    try:
        message = await channel.fetch_message(int(message_id))
    except discord.NotFound:
        log_manager.error("Message not found.")
        return

    embed = generate_updated_embed(bot, server_name, status, player_count, config_manager)
    await message.edit(embed=embed)

def generate_updated_embed(bot, server_name, status, player_count, config_manager):
    embed_config = config_manager.get('embed_setup')
    current_statuses = load_current_statuses()
    current_statuses[server_name] = {'status': status, 'players': player_count}
    save_current_statuses(current_statuses)

    embed = discord.Embed(title=embed_config['community_name'])
    for server in embed_config['servers']:
        server_status = current_statuses.get(server['name'], {"status": "Unknown", "players": "Unknown"})
        value = f"Status: {server_status['status']}\nPlayers Online: {server_status['players']}"
        embed.add_field(name=f"Server {server['name']}", value=value, inline=False)

    return embed

def load_current_statuses():
    try:
        with open('core/server_statuses.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        log_manager.error("Failed to load current statuses.")
        return {}

def save_current_statuses(statuses):
    with open('core/server_statuses.json', 'w') as file:
        json.dump(statuses, file)
        log_manager.info("Saved updated server statuses.")
