import discord
import os
from datetime import datetime
import pytz
from discord.ext import tasks
from bot_logger import log
from config import BOT_TIMEZONE, SERVER_NAME

class DiscordInterface:
    def __init__(self, bot, channel_id):
        self.bot = bot
        self.channel_id = channel_id
        self.status_message = None
        self.server_start_time = None
        # Get the directory path of the current file
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.status_message_id_file = os.path.join(self.current_directory, 'status_message_id.txt')

    def schedule_status_check(self, ark_server_manager):
        self.ark_server_manager = ark_server_manager
        self.status_check_loop.start()

    @tasks.loop(minutes=15)
    async def status_check_loop(self):
        if self.ark_server_manager.is_server_running():
            await self.update_status_embed('Online')
        else:
            await self.update_status_embed('Offline')

    @status_check_loop.error
    async def status_check_loop_error(self, error):
        await self.on_status_check_error(error)

    async def on_status_check_error(self, exception):
        log(f"Status check failed: {exception}", 'ERROR')

    async def post_status_embed(self, status):
        channel = self.bot.get_channel(self.channel_id)
        if not channel:
            print(f"Could not find channel with ID: {self.channel_id}")  # Debug print
            return

        # Check for an existing status message ID and try to fetch the message
        existing_message_id = self.get_existing_message_id()  # Method to implement
        if existing_message_id:
            try:
                self.status_message = await channel.fetch_message(existing_message_id)
                return
            except discord.NotFound:
            # If the message is not found, proceed to post a new one
                pass

        # If no existing message, post a new one
        embed = self.create_status_embed(status)
        self.status_message = await channel.send(embed=embed)
        self.store_message_id(self.status_message.id)  # Method to implement

    async def update_status_embed(self, status):
        if not self.status_message:
            await self.post_status_embed(status)
            return

        embed = self.create_status_embed(status)
        await self.status_message.edit(embed=embed)

    def create_status_embed(self, status):
        timezone = pytz.timezone(BOT_TIMEZONE)
        now = datetime.now(timezone)
        embed = discord.Embed(title=f"{SERVER_NAME} Server Status", color=0x00ff00)
        embed.add_field(name="Status", value=status, inline=False)
        embed.add_field(name="Last Updated", value=now.strftime(f'%Y-%m-%d %H:%M:%S {BOT_TIMEZONE}'), inline=False)

        if self.server_start_time:
            start_time_str = self.server_start_time.strftime(f'%Y-%m-%d %H:%M:%S {BOT_TIMEZONE}')
            embed.add_field(name="Server Started At", value=start_time_str, inline=False)
        else:
            embed.add_field(name="Server Started At", value="Not started since bot initialization", inline=False)

        embed.set_footer(text=f"All times are in {BOT_TIMEZONE}")
        return embed

    def set_server_start_time(self, start_time):
        self.server_start_time = start_time

    def store_message_id(self, message_id):
        with open(self.status_message_id_file, 'w') as file:
            file.write(str(message_id))

    def get_existing_message_id(self):
        try:
            with open(self.status_message_id_file, 'r') as file:
                return int(file.read().strip())
        except FileNotFoundError:
            return None