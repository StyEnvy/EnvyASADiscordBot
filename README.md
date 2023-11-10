# EnvyASADiscordBot
Discord bot for Ark Survival Ascended

We have a Discord bot designed to assist with managing our Ark: Survival Evolved server. Here are its key features:

Persistent Server Status Embed: The bot maintains an embed in a specified channel that shows the server's status (Online/Offline), last updated timestamp, and server start time. This embed updates in real time and remains consistent even if the bot is restarted.

Configurable Timezone: The timestamps in the embed use a configurable timezone, based on the PYTZ library, allowing you to set it as per your local time.

Server Control Commands: Admins can use commands to start, shut down (with a 5-minute warning), or restart the server directly from Discord.

The bot's focus is to provide a straightforward and reliable way to monitor and control your Ark server directly from Discord.

Setup instructions:

1. Open the EnvyGames folder
2. Open the .env folder with notepad++
3. Fill out the .env file and use the envreadme.txt and the timezonereadme.txt for assistance.
4. Use the run.bat to start the bot and enjoy

NOTE: You can setup automatic restart of the server by setting AUTO_RESTART_ON_CRASH=False to True in the .env

NOTE: You must create the discord role for administering the server, and set it in the .env for this function to work.

You can change the name of the root folder, but you cannot change the EnvyGames folder name within the bot. This will break functionality.

Join the Envy Games US Discord, grab the Envy Discord Bots role, and you'll see our section on our bot. 
https://discord.gg/seTY4VpXpp
