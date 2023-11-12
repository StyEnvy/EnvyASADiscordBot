# EnvyASADiscordBot
Discord bot for Ark Survival Ascended

MADE WITH PYTHON VERSION 3.11.5. THIS DOES NOT WORK WITH PYTHON VERSION 3.12.x AT THIS TIME. THIS BOT IS FOR WINDOWS OS. 

https://www.python.org/downloads/release/python-3115/
Note: When installing python remember to check the box for adding to PATH

We have a Discord bot designed to assist with managing our Ark: Survival Evolved server. Here are its key features:

Persistent Server Status Embed: The bot maintains an embed in a specified channel that shows the server's status (Online/Offline), last updated timestamp, and server start time. This embed updates in real time and remains consistent even if the bot is restarted.

Configurable Timezone: The timestamps in the embed use a configurable timezone, based on the PYTZ library, allowing you to set it as per your local time.

Configurable Server Auto-restart: The bot will restart the server if it detects it has gone down during a heartbeat check. Detection is based on whether or not the process for the server is running or not.

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

Python Installation and Virtual Environment Setup Guide for EnvyASADiscordBot:

To ensure full compatibility with EnvyASADiscordBot and all Python libraries it utilizes, it is crucial to install Python 3.11.x preferable 3.11.5. Please avoid using Python version 3.12.x, as it is not compatible with discord.py, primarily due to issues with aiohttp, which is a dependency of discord.py. You can download Python 3.11.5 from Python's official website: https://www.python.org/downloads/

Initial Step: Install Python 3.11.5
Before you start, make sure to install Python 3.11.5 on your computer. During the installation, remember to choose the option to add Python to your system PATH.

Setting Up with newenv.bat
The newenv.bat file simplifies setting up your bot. If you're not familiar with manual setups or prefer a quicker method, this is the recommended approach.

How to Use newenv.bat:

1. Ensure Python 3.11.5 is installed and properly set in your PATH.
2. Find and double-click the newenv.bat file in your bot's folder. 

This script will:
1. Check and create a new virtual environment if it doesn't exist.
2. Activate the virtual environment.
3. Install all necessary dependencies from the requirements.txt file.


Manual Setup (Optional)
If you'd rather set things up manually, here are the steps:

Python Installation:

1. Install Python 3.11.5 and ensure you select the option to Add Python to PATH.

Virtual Environment Setup:

1. Go to your bot's folder and delete the 'venv' folder if it's there.
2. Open PowerShell ISE.
3. Change Directory:

Type cd [YourEnvyASADiscordBotFolderPath] and press Enter.
Replace [YourEnvyASADiscordBotFolderPath] with the actual path to your bot's folder.

Create Virtual Environment:

1. Enter python -m venv venv and press Enter.

Activate Virtual Environment:

2. Enter .\venv\Scripts\Activate.ps1 and press Enter.

Install Dependencies:

3. Type pip install -r requirements.txt and press Enter.

Example Directory Structure:

Bot Folder: F:\ASADiscordBot\EnvyASADiscordBot
venv Folder: F:\ASADiscordBot\EnvyASADiscordBot\venv

Note: Ensure the 'venv' folder is created inside the '\EnvyASADiscordBot or \EnvyASADiscordBot-main' directory or whatever it is renamed to.