from contextlib import asynccontextmanager
from fastapi import FastAPI
from tqdm import tqdm
import asyncio

from semantictool.toolhost import init_tool_host, exit_tool_host, TOOL_HOST
from semantictool.semantic.model import VECTORMODEL
from semantictool.semantic.store import STORE
from semantictool.semantic.clusters import CLUSTER
from semantictool.semantic.embedder import process_tool, CONCURRENCY_LIMIT


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_tool_host()
    VECTORMODEL.load()

    tools = await TOOL_HOST.list_tools()
    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)

    tasks = [process_tool(tool, semaphore) for tool in tools]
    results = tqdm(await asyncio.gather(*tasks))

    for result in results:
        if result is None:
            continue
        name, vector = result
        try:
            await STORE.add(name, vector)
        except ValueError:
            pass

    await CLUSTER.fit(await STORE.get_all())

    yield
    await exit_tool_host()
