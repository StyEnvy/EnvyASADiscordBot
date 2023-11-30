import asyncio
from mcrcon import MCRcon
from core.logging.logger import LogManager

class ServerStopper:
    def __init__(self, server_info, log_manager, bot, user_id):
        self.server_info = server_info
        self.log_manager = log_manager
        self.bot = bot
        self.user_id = user_id

    async def stop_server(self):
        try:
            with MCRcon(self.server_info['rcon_ip'], self.server_info['rcon_password'], self.server_info['rcon_port']) as mcr:
                await self.send_shutdown_warnings(mcr)
                shutdown_successful = await self.execute_shutdown(mcr)
                if shutdown_successful:
                    self.log_manager.info(f"Shutdown command sent to Server {self.server_info['name']}.")
                else:
                    self.log_manager.error(f"Failed to execute shutdown command for Server {self.server_info['name']}.")
                    await self.send_failure_dm()
        except Exception as e:
            self.log_manager.error(f"Failed to stop Server {self.server_info['name']}: {e}")
            await self.send_failure_dm()

    async def send_shutdown_warnings(self, mcr):
        warning_times = self.server_info.get('warning_times', [])
        if not warning_times or len(warning_times) < 2:
            self.log_manager.error("Insufficient warning times configured.")
            return  # Need at least two warning times

        # Send the first warning immediately
        total_shutdown_time = warning_times[0] * 60
        mcr.command(f"serverchat Shutdown in {warning_times[0]} minutes. Please log out safely.")
        self.log_manager.info(f"Immediate shutdown warning sent to Server {self.server_info['name']}: {warning_times[0]} Minutes Until Shutdown.")

        # Wait until the second warning time
        await asyncio.sleep((warning_times[0] - warning_times[1]) * 60)
        mcr.command(f"serverchat Shutdown in {warning_times[1]} minutes. Please log out safely.")
        self.log_manager.info(f"Second shutdown warning sent to Server {self.server_info['name']}: {warning_times[1]} Minutes Until Shutdown.")

        # Final 10 second warning
        await asyncio.sleep((warning_times[1] * 60) - 10)
        mcr.command("serverchat Shutdown in 10 seconds. Please log out immediately.")
        self.log_manager.info("Final 10-second shutdown warning sent.")

    async def execute_shutdown(self, mcr):
        try:
            mcr.command("doexit")  # Sending shutdown command
            self.log_manager.info(f"Shutdown command sent to Server {self.server_info['name']}.")
            # Implement a brief delay to give the server time to start the shutdown process
            await asyncio.sleep(5)
            # Attempt to reconnect to the server as a secondary check
            try:
                with MCRcon(self.server_info['rcon_ip'], self.server_info['rcon_password'], self.server_info['rcon_port']) as test_mcr:
                    return False  # If this succeeds, the server didn't shut down
            except ConnectionRefusedError:
                return True  # Connection refused, so server is likely shutting down
        except Exception as e:
            self.log_manager.error(f"Error during shutdown of Server {self.server_info['name']}: {e}")
            return False

    async def send_failure_dm(self):
        try:
            user = await self.bot.fetch_user(self.user_id)
            await user.send(f"Shutdown of Server {self.server_info['name']} did not go through properly. Manual intervention required.")
        except Exception as e:
            self.log_manager.error(f"Failed to send DM to user with ID {self.user_id}: {e}")



