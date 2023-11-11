import subprocess
import psutil
import time
import os
from config import SERVER_EXECUTABLE, RCON_HOST, RCON_PORT, RCON_PASSWORD, AUTO_RESTART_ON_CRASH
from bot_logger import log
from mcrcon import MCRcon

class ArkServerManager:
    def __init__(self):
        self.process = None

    def start_server(self, user_info):
        try:
            # Check if the batch file exists and is accessible
            if not os.path.exists(SERVER_EXECUTABLE):
                log(f'Server executable not found: {SERVER_EXECUTABLE}', 'ERROR')
                return False

            # Start the server using the batch file
            subprocess.Popen([SERVER_EXECUTABLE])
            time.sleep(5)  # Wait for a few seconds to give the server time to start

            # Check if 'ArkAscendedServer.exe' is running
            server_running = False
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] == 'ArkAscendedServer.exe':
                    server_running = True
                    break

            if server_running:
                log(f'Server successfully started by {user_info}', 'INFO')
                return True
            else:
                log(f'Server failed to start by {user_info}. ArkAscendedServer.exe not found in processes.', 'ERROR')
                return False

        except PermissionError as perm_err:
            log(f'Permission denied error while starting the server by {user_info}: {perm_err}', 'ERROR')
            return False
        except FileNotFoundError as file_err:
            log(f'File not found error while starting the server by {user_info}: {file_err}', 'ERROR')
            return False
        except Exception as e:
            log(f'Unexpected error occurred while starting the server by {user_info}: {e}', 'ERROR')
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