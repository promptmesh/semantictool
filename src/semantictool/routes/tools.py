from fastapi import APIRouter

from semantictool.toolhost import TOOL_HOST
from semantictool.routes.models import Tool, ListToolsResponse

router = APIRouter(
    prefix="/tools",
)

@router.get("/list")
async def list_tools() -> ListToolsResponse:
    """List all tools."""

    raw_tools = await TOOL_HOST.list_tools()
    tools = [
        Tool.model_validate({
            "name": tool.name,
            "description": tool.description,
            "inputSchema": tool.inputSchema,
        })
        for tool in raw_tools
    ]
    return ListToolsResponse.model_validate({"tools": tools})
