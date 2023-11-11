import os

def load_env():
    # Construct the path to the .env file
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    # Check if the .env file exists
    if not os.path.isfile(env_path):
        raise FileNotFoundError(f"No such file or directory: '{env_path}'")
    
    with open(env_path, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

# Call the load_env function to load the environment variables
load_env()

# Retrieve the environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN') # No default value; must be set in .env
COMMAND_PREFIX = os.getenv('COMMAND_PREFIX') #Default is !
SERVER_EXECUTABLE = os.getenv('SERVER_EXECUTABLE') # No default value; must be set in .env
STATUS_CHANNEL_ID = int(os.getenv('STATUS_CHANNEL_ID')) # No default value; must be set in .env
ARK_ADMIN_ROLE = os.getenv('ARK_ADMIN_ROLE', 'Administrator')  # Default to Administrator if not set
BOT_TIMEZONE = os.getenv('BOT_TIMEZONE', 'US/Eastern')  # Default to 'US/Eastern' if not set
GAME_STATUS = os.getenv('GAME_STATUS', 'Ark Survival Ascended')  # Default to 'Ark Survival Ascended' if not set
SERVER_NAME = os.getenv('SERVER_NAME', 'Envy Games ASA Server')  # Default to 'Envy Games ASA Server' if not set
RCON_HOST = os.getenv('RCON_HOST')  # No default value; must be set in .env
RCON_PORT = int(os.getenv('RCON_PORT'))  # No default value; must be set in .env
RCON_PASSWORD = os.getenv('RCON_PASSWORD')  # No default value; must be set in .env
AUTO_RESTART_ON_CRASH = os.getenv('AUTO_RESTART_ON_CRASH', 'False') == 'True'  # Defaults to False if not set
STATUS_CHECK_INTERVAL = int(os.getenv('STATUS_CHECK_INTERVAL', 15))