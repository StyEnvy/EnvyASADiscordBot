import subprocess
import psutil
import time
import os
import asyncio
from config import SERVER_EXECUTABLE, RCON_HOST, RCON_PORT, RCON_PASSWORD, AUTO_RESTART_ON_CRASH, RESTART_DELAY
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

        return False

    async def check_and_restart_server(self):
        if not self.is_server_running():
            if AUTO_RESTART_ON_CRASH:
                log('Server appears to be down. Attempting automatic restart...', 'INFO')
                user_info = 'Auto-Restart System'
                return await self.start_server(user_info)
            else:
                log('Server appears to be down.', 'INFO')
                return False
        return True

    def send_rcon_command(self, command):
        with MCRcon(RCON_HOST, RCON_PASSWORD, RCON_PORT) as mcr:
            resp = mcr.command(command)
            log(f'RCON command response: {resp}', 'INFO')
            return resp

    async def shutdown_server(self):
        try:
            # Issue the shutdown command
            shutdown_response = self.send_rcon_command("DoExit")

            # Wait for the server process to shut down
            while self.is_server_running():
                await asyncio.sleep(1)  # Non-blocking wait for one second

            # Log and return the response
            log(f'Shutdown command response: {shutdown_response}', 'INFO')
            return shutdown_response
        except Exception as e:
            log(f'Error during server shutdown: {e}', 'ERROR')
            return False

    async def restart_server(self, user_info):
        try:
            if await self.shutdown_server():
                log(f"Server shutdown initiated by {user_info}", 'INFO')
                await asyncio.sleep(RESTART_DELAY)  # Use asyncio.sleep for non-blocking wait
                return await self.start_server(user_info)
            else:
                log("Server shutdown failed during restart.", 'ERROR')
                return False
        except Exception as e:
            log(f"Error during server restart: {e}", 'ERROR')
            return False