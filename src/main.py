from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.api.router import api_router
from src.core.config import Settings
from src.core.dependencies import create_container
from src.core.lifespan import lifespan
from src.core.logging import configure_logging

app = FastAPI(
    title="Incidentor",
    version="1.0.0",
    lifespan=lifespan,
)
configure_logging(Settings())
setup_dishka(container=create_container(), app=app)
app.include_router(api_router)
