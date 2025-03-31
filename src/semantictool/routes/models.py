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
