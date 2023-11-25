# EnvyASADiscordBot
Discord bot for Ark Survival Ascended

This bot was made with Python Version 3.11.5 and the Discord.py library for Python.

Setup instructions:

The setup for the bot is now done in the config.json file. Please open it with notepad++ or your favorite editing software.

token = Your discord bot token
prefix = Moot as we do not use commands to start/stop the server anymore
Community Name = This is the Title of the status embed for your servers


1 server setup example

    "embed_setup": {
      "community_name": "Envy Games US",
      "servers": [
        {
            "name": "ServerName1",
            "address": "127.0.0.1",
            "rconport": "12345",
            "rconpassword": "Password"
          }
      ],
      
2 server setup example

    "embed_setup": {
      "community_name": "Envy Games US",
      "servers": [
        {
            "name": "ServerName1",
            "address": "127.0.0.1",
            "rconport": "12345",
            "rconpassword": "Password"
          },
          {
            "name": "ServerName2",
            "address": "127.0.0.1",
            "rconport": "12345",
            "rconpassword": "Password"
          }
      ],

  If you wish to add/remove servers you can. This embed now supports dynamically adding/removing servers based on whats in the config. Do not confused this with the server_control section as they are not connected programmatically.

rconpassword = your server's admin password
embed_channel_id = The discord channel ID where you want your embed to be posted
status_check_interval = Time in seconds for the embed's status update

The server_control section of the configuration is responsible for setting up and managing server start/stop functionalities. It is an array where each element represents a server with its specific control settings. This configuration dynamically generates start and stop control buttons for each server and posts them to a specified Discord channel. Each server in the array generates a pair of buttons, allowing for individual control over its operations.
Structure and Explanation

    servers: This is an array where each element represents a server. Each server element contains several fields:
        batch_path: The path to the batch file used to start the server.
        rcon_port: The port used for RCON (Remote Console) connections to the server.
        rcon_ip: The IP address for RCON connections.
        rcon_password: The password for RCON access.
        warning_times: An array of two numbers. The first number is the total time before the server shuts down, and the second number is the time remaining for the first warning. A final warning is automatically sent 10 seconds before shutdown.

    control_channel_id: The Discord channel ID where the control buttons (Start/Stop) for each server will be posted.

    required_role: The name of the Discord role required to use the control buttons. Only users with this role can start or stop servers.

Dynamic Button Generation:

When the bot starts, it checks the server_control configuration and generates a set of Start and Stop buttons for each server listed. These buttons are then posted as separate messages in the Discord channel specified by control_channel_id. Each message corresponds to a server and contains two buttons: one for starting and one for stopping that particular server.

The bot ensures that the correct number of button sets is posted. If a server is added or removed from the configuration, the bot will adjust accordingly, adding or removing button messages to match the current configuration.

Shutdown Warning Timers (warning_times) continued:

The warning_times configuration controls the timing of shutdown warning messages for a server. This setting is an array with two values, representing minutes. These values determine when warning messages are sent to the server before a shutdown occurs. The sequence of warnings is as follows:

    Total Duration (X minutes): The first number in the array represents the total duration before the server shuts down. This is the period from when the shutdown process starts to when the server is actually turned off.

    First Warning (Y minutes remaining): The second number in the array specifies when the first warning message is sent, indicating the remaining time until shutdown. This warning is issued when there are Y minutes left until the server shutdown.

    Final Warning (10 seconds remaining): Regardless of the configured times, a final warning is always sent 10 seconds before the actual shutdown.
