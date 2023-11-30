import subprocess
from core.config_manager import ConfigManager
from core.logging.logger import LogManager

class ServerStarter:
    def __init__(self, server_info, log_manager):
        self.server_info = server_info
        self.log_manager = log_manager

    def start_server(self):
        if self.server_info.get('batch_path'):
            try:
                subprocess.Popen(self.server_info['batch_path'], shell=True)
                self.log_manager.info(f"Starting Server {self.server_info['name']}.")
            except Exception as e:
                self.log_manager.error(f"Failed to start Server {self.server_info['name']}: {e}")
        else:
            self.log_manager.error(f"Batch path not found for Server {self.server_info['name']}.")
