import subprocess
import psutil
import time
from config import SERVER_EXECUTABLE, RCON_HOST, RCON_PORT, RCON_PASSWORD, AUTO_RESTART_ON_CRASH
from bot_logger import log
from mcrcon import MCRcon

class ArkServerManager:
    def __init__(self):
        self.process = None

    def start_server(self, user_info):
        try:
            # The SERVER_EXECUTABLE should be the path to the batch file that starts the server
            self.process = subprocess.Popen([SERVER_EXECUTABLE], creationflags=subprocess.CREATE_NEW_CONSOLE)
            log(f'Server started by {user_info} with PID: {self.process.pid}', 'INFO')
            return True
        except Exception as e:
            log(f'Failed to start the server by {user_info}: {e}', 'ERROR')
            return False

    def is_server_running(self):
        # Check if 'ArkAscendedServer.exe' is among the running processes
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'ArkAscendedServer.exe':
                return True

        # If the server is not running, check if auto-restart is enabled
        if AUTO_RESTART_ON_CRASH:
            log('Server appears to be down. Attempting automatic restart...', 'INFO')
            user_info = 'Auto-Restart System'
            self.start_server(user_info)
            return True

        return False

    def send_rcon_command(self, command):
        with MCRcon(RCON_HOST, RCON_PASSWORD, RCON_PORT) as mcr:
            resp = mcr.command(command)
            log(f'RCON command response: {resp}', 'INFO')
            return resp

    def shutdown_server(self):
        # Issue the shutdown command
        shutdown_response = self.send_rcon_command("DoExit")
        
        # Wait for the server process to shut down
        while self.is_server_running():
            time.sleep(1)  # Check every second
        
        # Log and return the response
        log(f'Shutdown command response: {shutdown_response}', 'INFO')
        return shutdown_response

    def restart_server(self, user_info):
        if self.shutdown_server():
            # Wait for 10 seconds after the server shuts down
            time.sleep(10)
            # Start the server again
            return self.start_server(user_info)
        else:
            return False