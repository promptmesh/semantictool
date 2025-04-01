from pydantic import AnyUrl, BaseModel
from easymcp.client.SessionMaker import transportTypes

class ConfigUrl(AnyUrl):
    allowed_schemes = {'file', 'http', 'https'}

class ConfigLocation(BaseModel):
    path: ConfigUrl

class vectorModel(BaseModel):
    model_name: str = "all-MiniLM-L6-v2"
    dim: int = 384

class config(BaseModel):
    mcp_servers: dict[str, transportTypes]
    embedding: vectorModel