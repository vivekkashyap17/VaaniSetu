import time

from fastapi import APIRouter

from app.core.logging.logger import setup_logger

from app.schemas.translation import (
    TranslationRequest,
    TranslationResponse
)

from app.pipelines.translation_pipeline import TranslationPipeline

from app.utils.async_inference import run_inference_async

from app.core.analytics.analytics_manager import AnalyticsManager


router = APIRouter()

logger = setup_logger()



@router.post(
    "/translate",
    response_model=TranslationResponse
)
async def translate_text(request: TranslationRequest):

    start_time = time.time()

    logger.info("Translation request received")

    pipeline = TranslationPipeline()

    pipeline_output = await run_inference_async(
        pipeline.run,
        request.text
)
    

    processed_text = pipeline_output["processed_text"]

    detected_language = pipeline_output["detected_language"]

    transliterated_text = pipeline_output["transliterated_text"]

    translated_output = pipeline_output["translated_text"]

    confidence_score = pipeline_output["confidence_score"]

    cache_hit = pipeline_output["cache_hit"]

    processing_time = round(time.time() - start_time, 4)

    AnalyticsManager.record_request(
    language=detected_language,
    latency=processing_time,
    cache_hit=cache_hit
)

    return TranslationResponse(
        original_text=request.text,
        translated_text=translated_output,
        transliterated_text=transliterated_text,
        detected_language=detected_language,
        confidence_score=confidence_score,
        target_language=request.target_language,
        processing_time=processing_time
    )