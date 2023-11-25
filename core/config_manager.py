import json
from core.logging.logger import LogManager

class ConfigManager:
    def __init__(self, config_file):
        self.config_file = config_file
        self.log_manager = LogManager()
        self.config = self.load_config()

    def load_config(self):
        try:
            with open(self.config_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            self.log_manager.error(f"Configuration file {self.config_file} not found.")
            return {}  # Return an empty dict if the file is not found
        except json.JSONDecodeError:
            self.log_manager.error("Invalid JSON in the configuration file.")
            return {}  # Return an empty dict if JSON is invalid

    def get(self, *keys):
        config_section = self.config
        for key in keys:
            config_section = config_section.get(key, None)
            if config_section is None:
                return None
        return config_section
