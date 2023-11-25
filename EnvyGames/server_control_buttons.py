import discord
from core.config_manager import ConfigManager

config_manager = ConfigManager('config.json')

def create_server_control_buttons(server_index):
    view = discord.ui.View()
    start_button = discord.ui.Button(label=f"Start Server {server_index + 1}", style=discord.ButtonStyle.green, custom_id=f"start_{server_index}")
    stop_button = discord.ui.Button(label=f"Stop Server {server_index + 1}", style=discord.ButtonStyle.red, custom_id=f"stop_{server_index}")
    view.add_item(start_button)
    view.add_item(stop_button)
    return view

def process_button_interaction(interaction):
    custom_id = interaction.component.custom_id
    server_number = int(custom_id.split("_")[1])

    if custom_id.startswith("start_"):
        # Logic to start the server
        return f"Starting Server {server_number + 1}"
    elif custom_id.startswith("stop_"):
        # Logic to stop the server
        return f"Stopping Server {server_number + 1}"
