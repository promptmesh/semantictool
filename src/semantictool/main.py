from fastapi import FastAPI

from semantictool.lifespan import lifespan
from semantictool.routes import router
from semantictool.telemetry import setup_tracing

from loguru import logger
logger.disable("easymcp")

app = FastAPI(
    title="Semantic Tool",
    description="A tool management platform.",
    version="0.0.1",
    lifespan=lifespan,
)

setup_tracing(app)

app.include_router(router)