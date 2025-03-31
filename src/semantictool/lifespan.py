from contextlib import asynccontextmanager
from fastapi import FastAPI
from semantictool.toolhost import init_tool_host, exit_tool_host

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_tool_host()
    yield
    await exit_tool_host()