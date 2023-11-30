import discord
import json
from core.config_manager import ConfigManager
from core.logging.logger import LogManager
from .server_control_buttons import create_server_control_buttons

log_manager = LogManager()
config_manager = ConfigManager('config.json')

async def handle_server_control_buttons(bot):
    control_channel_id = config_manager.get('server_control', 'control_channel_id')
    control_channel = bot.get_channel(int(control_channel_id))
    if not control_channel:
        log_manager.error("Server control channel not found.")
        return

    servers = config_manager.get('server_control', 'servers')
    stored_ids = []

    # Load existing message IDs
    try:
        with open('core/server_control_message_id.json', 'r') as file:
            stored_ids = json.load(file).get('message_ids', [])
    except (FileNotFoundError, json.JSONDecodeError):
        stored_ids = []

    # Check if stored messages exceed the number of configured servers
    if len(stored_ids) > len(servers):
        # Delete extra messages
        for message_id in stored_ids[len(servers):]:
            try:
                message = await control_channel.fetch_message(int(message_id))
                await message.delete()
                log_manager.info(f"Deleted outdated server control button message (ID: {message_id}).")
            except discord.NotFound:
                log_manager.error(f"Could not find message with ID {message_id} to delete.")
        stored_ids = stored_ids[:len(servers)]

    # Update or create new button messages
    for index, server in enumerate(servers):
        server_name = server.get('name', f'Server {index + 1}')  # Fallback to 'Server {index+1}' if 'name' is not present
        try:
            message_id = stored_ids[index] if index < len(stored_ids) else None
            if message_id:
                message = await control_channel.fetch_message(int(message_id))
                log_manager.info(f"Updating server control buttons for {server_name}.")
                # Update the message with new buttons
                view = create_server_control_buttons(index)
                await message.edit(content=f"{server_name} Control Buttons:", view=view)
            else:
                raise FileNotFoundError
        except (FileNotFoundError, discord.NotFound):
            log_manager.info(f"Posting new server control buttons for {server_name}.")
            view = create_server_control_buttons(index)
            button_message = await control_channel.send(f"{server_name} Control Buttons:", view=view)
            if index < len(stored_ids):
                stored_ids[index] = button_message.id
            else:
                stored_ids.append(button_message.id)

    # Save updated message IDs
    with open('core/server_control_message_id.json', 'w') as file:
        json.dump({'message_ids': stored_ids}, file)
