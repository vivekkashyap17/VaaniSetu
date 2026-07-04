from fastapi import APIRouter

from app.core.logging.logger import setup_logger

from app.schemas.health import HealthResponse


router = APIRouter()

logger = setup_logger()


@router.get(
    "/health",
    response_model=HealthResponse
)
async def health_check():

    logger.info("Health check endpoint accessed")

    return HealthResponse(
        status="healthy",
        service="VaaniSetu"
    )