import logging
from logging.handlers import RotatingFileHandler
import os

class LogManager:
    _logger = None  # Class-level logger

    def __init__(self, log_file='envygames.log', max_size=1024*1024*5, backup_count=10):
        self.log_file = log_file
        self.max_size = max_size
        self.backup_count = backup_count
        if not LogManager._logger:
            LogManager._logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger('EnvyASA')
        logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture all levels of logs

        # Ensure log directory exists
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # Handler for rotating logs
        handler = RotatingFileHandler(
            filename=f'logs/{self.log_file}', 
            maxBytes=self.max_size, 
            backupCount=self.backup_count
        )
        handler.setFormatter(logging.Formatter(
            '%(asctime)s:%(levelname)s:%(name)s: %(message)s'
        ))

        logger.addHandler(handler)
        return logger

    # Convenience methods for logging at various levels
    def debug(self, message):
        LogManager._logger.debug(message)

    def info(self, message):
        LogManager._logger.info(message)

    def warning(self, message):
        LogManager._logger.warning(message)

    def error(self, message):
        LogManager._logger.error(message)
