from fastapi import APIRouter, HTTPException, Body
from opentelemetry import trace
from mcp.types import CallToolResult

from semantictool.semantic.clusters import CLUSTER
from semantictool.semantic.store import STORE
from semantictool.toolhost import TOOL_HOST
from semantictool.routes.models import SemanticClustersResponse, SemanticToolSearchRequest, SemanticToolSearchResponse, Tool, ListToolsResponse, ToolCallRequest
from semantictool.semantic.model import VECTORMODEL

tracer = trace.get_tracer(__name__)

router = APIRouter(
    prefix="/tools",
)

@router.get("/list")
async def list_tools() -> ListToolsResponse:
    """List all tools."""

    with tracer.start_as_current_span("list-tools"):
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
        with tracer.start_as_current_span("tool-call"):
            result = await TOOL_HOST.call_tool(req.name, args)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tool call failed: {e}")
    
@router.post("/semantic")
async def semantic_search(req: SemanticToolSearchRequest = Body(...)) -> SemanticToolSearchResponse:
    """Search for tools based on semantic similarity."""
    response = []

    with tracer.start_as_current_span("vector-embedding"):
        vector = await VECTORMODEL.embed(req.query)

    with tracer.start_as_current_span("store-search"):
        tools = await STORE.search(vector, req.quantity)

    with tracer.start_as_current_span("metadata-matching"):
        actualtools = await TOOL_HOST.list_tools()
        actualtools_map = {tool.name: tool for tool in actualtools}

        for tool in tools:
            actualtool = actualtools_map.get(tool)
            if actualtool:
                response.append(Tool.model_validate({
                    "name": actualtool.name,
                    "description": actualtool.description,
                    "inputSchema": actualtool.inputSchema,
                }))

    return SemanticToolSearchResponse.model_validate({"tools": response})

@router.post("/semantic/clusters")
async def semantic_clusters() -> SemanticClustersResponse:
    """Discover duplicate tools via semantic similarity using DBSCAN."""
    clusters = await CLUSTER.get()
    if not clusters:
        raise HTTPException(status_code=500, detail="No clusters available")
    return SemanticClustersResponse.model_validate({"clusters": list(clusters.values())})
