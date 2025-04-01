from fastapi import APIRouter
from semantictool.routes.tools import router as tools_router
from semantictool.routes.servers import router as servers_router

router = APIRouter(
    prefix="/api/v1",
)

router.include_router(servers_router)
router.include_router(tools_router)