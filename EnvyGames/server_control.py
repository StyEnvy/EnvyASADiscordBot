import subprocess
from core.config_manager import ConfigManager
from core.logging.logger import LogManager
from mcrcon import MCRcon
import time
import asyncio

config_manager = ConfigManager('config.json')
log_manager = LogManager()

def start_server(server_index):
    servers = config_manager.get('server_control', 'servers')
    if server_index < len(servers):
        server_info = servers[server_index]
        if server_info.get('batch_path'):
            try:
                subprocess.Popen(server_info['batch_path'], shell=True)
                log_manager.info(f"Starting Server {server_index + 1}.")
            except Exception as e:
                log_manager.error(f"Failed to start Server {server_index + 1}: {e}")
        else:
            log_manager.error(f"Batch path not found for Server {server_index + 1}.")
    else:
        log_manager.error(f"Server configuration not found for index {server_index}.")

async def stop_server(server_index):
    servers = config_manager.get('server_control', 'servers')
    if server_index < len(servers):
        server_info = servers[server_index]
        try:
            with MCRcon(server_info['rcon_ip'], server_info['rcon_password'], server_info['rcon_port']) as mcr:
                warning_times = sorted(server_info.get('warning_times', []), reverse=True)
                total_time = max(warning_times, default=0)

                for warning in warning_times:
                    wait_time = total_time - warning
                    await asyncio.sleep(wait_time * 60)
                    mcr.command(f"serverchat Shutdown in {warning} minutes. Please log out safely.")
                    log_manager.info(f"Shutdown warning sent to Server {server_index + 1}: {warning} Minutes Until Shutdown.")
                    total_time = warning

                # Final 10 second warning
                if total_time > 0:
                    await asyncio.sleep(total_time * 60)
                await asyncio.sleep(10)
                mcr.command("serverchat Shutdown in 10 seconds. Please log out immediately.")
                log_manager.info(f"Shutdown warning sent to Server {server_index + 1}: 10 Seconds Until Shutdown.")
                
                # Execute shutdown command
                mcr.command("doexit")
                log_manager.info(f"Shutdown command sent to Server {server_index + 1}.")
        except Exception as e:
            log_manager.error(f"Failed to stop Server {server_index + 1}: {e}")
    else:
        log_manager.error(f"Server configuration not found for index {server_index}.")



