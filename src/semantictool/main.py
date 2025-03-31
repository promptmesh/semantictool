from fastapi import FastAPI

from semantictool.lifespan import lifespan

app = FastAPI(
    title="Semantic Tool",
    description="A tool management platform.",
    version="0.0.1",
    lifespan=lifespan,
)