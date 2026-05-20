from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.root import router as root_router
from app.api.routes.health import router as health_router
from app.api.routes.translation import router as translation_router

from app.core.config.settings import get_settings
from app.core.logging.logger import setup_logger

from app.core.models.model_manager import ModelManager

from app.api.routes.analytics import router as analytics_router

from app.db.init_db import initialize_database


settings = get_settings()

logger = setup_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Starting BhashaBridge backend")
    
    ModelManager.load_models()

    initialize_database()

    yield

    logger.info("Shutting down BhashaBridge backend")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered multilingual translation backend for Indian local languages and dialects",
    lifespan=lifespan
)


app.include_router(root_router, prefix="/api/v1")

app.include_router(health_router, prefix="/api/v1")

app.include_router(translation_router, prefix="/api/v1")

app.include_router(analytics_router)