from fastapi import APIRouter, HTTPException, Body
from mcp.types import CallToolRequestParams, CallToolResult

from semantictool.toolhost import TOOL_HOST
from semantictool.routes.models import Tool, ListToolsResponse, ToolCallRequest

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


@router.post("/call", response_model=CallToolResult)
async def call_tool(req: ToolCallRequest = Body(...)) -> CallToolResult:
    try:
        args = req.arguments or {}
        result = await TOOL_HOST.call_tool(req.name, args)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tool call failed: {e}")