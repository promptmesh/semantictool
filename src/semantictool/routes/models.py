from pydantic import BaseModel

class Tool(BaseModel):
    name: str
    description: str
    inputSchema: dict

class ListToolsResponse(BaseModel):
    tools: list[Tool]

class ToolCallRequest(BaseModel):
    name: str
    arguments: dict

class Server(BaseModel):
    name: str

class ListServersResponse(BaseModel):
    servers: list[Server]

class SemanticToolSearchRequest(BaseModel):
    query: str
    quantity: int = 1

class SemanticToolSearchResponse(BaseModel):
    tools: list[Tool]


class SemanticClustersResponse(BaseModel):
    clusters: list[list[str]]