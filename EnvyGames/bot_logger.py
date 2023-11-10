import logging
from logging.handlers import RotatingFileHandler
import os

# Get the directory path of the current file (bot.py)
current_directory = os.path.dirname(os.path.abspath(__file__))

# Set the log file name with the full path
LOG_FILENAME = os.path.join(current_directory, 'bot_logs.log')
MAX_BYTES = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 5  # Keep five old log files

logger = logging.getLogger('discord_bot')
logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler(LOG_FILENAME, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

def log(message, level):
    if level == 'INFO':
        logger.info(message)
    elif level == 'ERROR':
        logger.error(message)
    else:
        raise ValueError(f"Logging level '{level}' is not supported.")
