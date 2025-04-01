from fastapi import APIRouter

from semantictool.toolhost import TOOL_HOST
from semantictool.routes.models import ListServersResponse

router = APIRouter(
    prefix="/servers",
)

@router.get("/list")
async def list_servers() -> ListServersResponse:
    """List all servers."""
    servers = []
    for server in TOOL_HOST.sessions.keys():
        servers.append({"name": server})
    return ListServersResponse.model_validate({"servers": servers})