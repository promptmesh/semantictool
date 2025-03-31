from fastapi import APIRouter
from semantictool.routes.tools import router as tools_router

router = APIRouter(
    prefix="/api/v1",
)

router.include_router(tools_router)