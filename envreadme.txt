COMMAND_PREFIX=! 

1.You can leave this as ! or change it.

BOT_TOKEN=

1.Go to the Discord Developer Portal https://discord.com/developers/applications
2.Click on the “New Application” button.
3.Give your application a name and click “Create”.
4.Inside your application, navigate to the “Bot” tab on the left-hand side.
5.Click on “Add Bot” and confirm by clicking “Yes, do it!”.
6.You have now created a bot user.
7.Under the “Bot” tab, you’ll see a section called “TOKEN” with a link to “Copy” the token.
8.Click “Copy” to copy your bot token. Keep this token private as it allows control over your bot.
9.Still under the “Bot” tab, you’ll find the “Privileged Gateway Intents” section.
10.Enable the toggles for “PRESENCE INTENT” and “SERVER MEMBERS INTENT”.
11.These are required for certain functionalities like tracking user presence or getting member lists.
12.Navigate to the “OAuth2” tab and select “URL Generator” from the left-hand side.
13.Under “SCOPES”, select “bot”.
14.In the “BOT PERMISSIONS” section, select the permissions your bot needs.
15.Copy the generated URL under “SCOPES”, paste it into your web browser, and select the server to invite your bot.

SERVER_EXECUTABLE=

1. EXAMPLE: C:\\SteamLibrary\\steamapps\\common\\ARK Survival Ascended Dedicated Server\\ServerRun.bat
2. As shown above, this is the run.bat or run.sh you use to start your server. You must use the format shown above.

STATUS_CHANNEL_ID=

1.Turn on developer mode in Discord if you haven’t already.
2. Go to your Discord server and right-click the text channel where you want the server status messages to appear.
3. Select “Copy ID” from the menu.
4. Paste the ID into the STATUS_CHANNEL_ID field in the .env file.

ARK_ADMIN_ROLE=

Make a new role or use an existing role. This role will be able to use the start, stop and restart commands.

BOT_TIMEZONE=America/New_York

You can leave this default for EST.
Please read the timezonereadme.txt file for more information.

GAME_STATUS=Ark Survival Ascended

1.If for some reason you want it to say something other than ASA you can change this. 

SERVER_NAME=The Island

1.This is the name of your server. It will be displayed in the status message embed.


Make sure you enable RCON in your gameusersettings.ini file!

RCON_HOST=The server IP address. 

1.If you are hosting this within your local network it is recommended to use your local IP, and not your public IP. WC states this can cause issues.

RCON_PORT= This is the RCON port you have set for your server.

RCON_PASSWORD= This is your server admin password. 

1.This is not the same as your server password. If you do not have a server admin password set, you can set one in your server config file.