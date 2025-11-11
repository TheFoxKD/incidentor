from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from src.api.v1.incidents import router as incidents_router

api_v1_router = APIRouter(prefix="/api/v1", route_class=DishkaRoute)
api_v1_router.include_router(incidents_router)
