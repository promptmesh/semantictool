from contextlib import asynccontextmanager
from fastapi import FastAPI
from tqdm import tqdm

from semantictool.toolhost import init_tool_host, exit_tool_host, TOOL_HOST
from semantictool.semantic.model import VECTORMODEL
from semantictool.semantic.store import STORE
from semantictool.semantic.clusters import CLUSTER

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_tool_host()
    VECTORMODEL.load()

    tools = tqdm(await TOOL_HOST.list_tools())

    for tool in tools:
        vectors = await VECTORMODEL.embed(tool.description)
        try:
            await STORE.add(tool.name, vector=vectors)
        except ValueError:
            pass

    await CLUSTER.fit(await STORE.get_all())

    yield
    await exit_tool_host()