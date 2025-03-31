from easymcp.client.ClientManager import ClientManager

from .config.loader import CONFIG

TOOL_HOST = ClientManager()

async def init_tool_host():
    await TOOL_HOST.init(CONFIG.mcp_servers)

async def exit_tool_host():
    for session in TOOL_HOST.sessions.keys():
        await TOOL_HOST.remove_server(session)