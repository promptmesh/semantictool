from contextlib import asynccontextmanager
from fastapi import FastAPI

from semantictool.toolhost import init_tool_host, exit_tool_host, TOOL_HOST
from semantictool.semantic.model import VECTORMODEL
from semantictool.semantic.store import STORE

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_tool_host()
    VECTORMODEL.load()

    for tool in (await TOOL_HOST.list_tools()):
        await STORE.add(tool.name, await VECTORMODEL.embed(tool.description))

    yield
    await exit_tool_host()