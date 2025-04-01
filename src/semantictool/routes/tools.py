from fastapi import APIRouter, HTTPException, Body
from mcp.types import CallToolResult

from semantictool.semantic.store import STORE
from semantictool.toolhost import TOOL_HOST
from semantictool.routes.models import SemanticToolSearchRequest, SemanticToolSearchResponse, Tool, ListToolsResponse, ToolCallRequest
from semantictool.semantic.model import VECTORMODEL

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
    
@router.post("/semantic")
async def semantic_search(req: SemanticToolSearchRequest = Body(...)) -> SemanticToolSearchResponse:
    """Search for tools based on semantic similarity."""
    response = []
    
    vector = await VECTORMODEL.embed(req.query)
    tools = await STORE.search(vector, req.quantity)
    actualtools = await TOOL_HOST.list_tools()
    for tool in tools:
        for actualtool in actualtools:
            if actualtool.name == tool:
                response.append(Tool.model_validate({
                    "name": actualtool.name,
                    "description": actualtool.description,
                    "inputSchema": actualtool.inputSchema,
                }))
            
    return SemanticToolSearchResponse.model_validate({"tools": response})