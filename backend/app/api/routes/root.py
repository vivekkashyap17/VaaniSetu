from fastapi import APIRouter

from app.core.logging.logger import setup_logger
from app.core.config.settings import get_settings


router = APIRouter()

logger = setup_logger()

settings = get_settings()


@router.get("/")
async def root():

    logger.info("Root endpoint accessed")

    return {
        "message": f"{settings.APP_NAME} Backend Running Successfully"
    }