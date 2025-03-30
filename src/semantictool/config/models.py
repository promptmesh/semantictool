from pydantic import AnyUrl, BaseModel
from easymcp.client.SessionMaker import transportTypes

class ConfigUrl(AnyUrl):
    allowed_schemes = {'file', 'http', 'https'}

class ConfigLocation(BaseModel):
    path: ConfigUrl

class config(BaseModel):
    mcp_servers: dict[str, transportTypes]
