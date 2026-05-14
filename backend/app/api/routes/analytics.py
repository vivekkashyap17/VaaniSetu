from fastapi import APIRouter

from app.core.analytics.analytics_manager import AnalyticsManager


router = APIRouter()


@router.get("/analytics")

async def get_analytics():

    return AnalyticsManager.get_metrics()