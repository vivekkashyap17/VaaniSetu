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

from app.core.vectorstore.embedding_manager import EmbeddingManager

from app.core.vectorstore.faiss_manager import FAISSManager

from app.api.routes.search import router as search_router

from app.services.llm.translation_refiner import TranslationRefiner

from fastapi.middleware.cors import CORSMiddleware

from slowapi.errors import RateLimitExceeded

from slowapi.middleware import SlowAPIMiddleware

from slowapi.extension import _rate_limit_exceeded_handler

from app.core.security.rate_limiter import limiter


settings = get_settings()

logger = setup_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Starting BhashaBridge backend")
    
    ModelManager.load_models()

    initialize_database()

    EmbeddingManager.load_embedding_model()

    FAISSManager.initialize_index()

    TranslationRefiner.load_refinement_model()

    yield

    logger.info("Shutting down BhashaBridge backend")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered multilingual translation backend for Indian local languages and dialects",
    lifespan=lifespan
)


allowed_origins = [
    origin.strip()
    for origin in settings.ALLOWED_ORIGINS.split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

app.add_middleware(SlowAPIMiddleware)


app.include_router(root_router, prefix="/api/v1")

app.include_router(health_router, prefix="/api/v1")

app.include_router(translation_router, prefix="/api/v1")

app.include_router(analytics_router)

app.include_router(search_router)