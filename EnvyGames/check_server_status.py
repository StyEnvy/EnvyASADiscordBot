from mcrcon import MCRcon

async def check_server_status(server):
    try:
        with MCRcon(server['address'], server['rconpassword'], int(server['rconport'])) as mcr:
            response = mcr.command("listplayers")
            players = parse_player_list(response)
            return 'Online', players
    except Exception:
        return 'Offline', 0

def parse_player_list(response):
    lines = response.split('\n')[2:]  # Skip the first two lines (RCON reply)
    return len(lines)  # Count of players
