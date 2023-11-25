import discord
from core.logging.logger import LogManager

def generate_server_embed(config):
    log_manager = LogManager()
    embed = discord.Embed(title=config['community_name'])
    
    for server in config['servers']:
        embed.add_field(
            name=f"Server {server['name']}",
            value="Status: Updating...\nPlayers Online: Updating...",  # Placeholder text
            inline=False
        )
    log_manager.info("Server embed generated.")
    
    return embed
