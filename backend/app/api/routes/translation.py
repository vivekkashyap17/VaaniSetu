import time

from requests import request

from fastapi import APIRouter

from app.core.logging.logger import setup_logger

from app.schemas.translation import (
    TranslationRequest,
    TranslationResponse
)

from app.pipelines.translation_pipeline import TranslationPipeline

from app.utils.async_inference import run_inference_async

from app.core.analytics.analytics_manager import AnalyticsManager

from app.db.repositories.translation_repository import TranslationRepository

from app.core.vectorstore.embedding_manager import EmbeddingManager

from app.core.vectorstore.faiss_manager import FAISSManager

from fastapi import Depends

from fastapi import Request

from app.core.security.api_key import verify_api_key

from app.core.security.rate_limiter import limiter


router = APIRouter()

logger = setup_logger()



@router.post(
    "/translate",
    response_model=TranslationResponse
)
@limiter.limit("5/minute")

async def translate_text(
    request: Request,
    translation_request: TranslationRequest,
    api_key: str = Depends(verify_api_key)
):

    start_time = time.time()

    logger.info("Translation request received")

    pipeline = TranslationPipeline()

    pipeline_output = await run_inference_async(
        pipeline.run,
        translation_request.text
)
    

    processed_text = pipeline_output["processed_text"]

    detected_language = pipeline_output["detected_language"]

    transliterated_text = pipeline_output["transliterated_text"]

    translated_output = pipeline_output["translated_text"]

    confidence_score = pipeline_output["confidence_score"]

    cache_hit = pipeline_output["cache_hit"]

    retrieved_contexts = (
    pipeline_output["retrieved_contexts"]
)

    semantic_context = (
    pipeline_output["semantic_context"]
)
    
    refined_translation = (
    pipeline_output["refined_translation"]
)

    processing_time = round(time.time() - start_time, 4)
    

    AnalyticsManager.record_request(
    language=detected_language,
    latency=processing_time,
    cache_hit=cache_hit
)
    
    TranslationRepository.save_translation(
    original_text=translation_request.text,
    translated_text=translated_output,
    detected_language=detected_language,
    confidence_score=confidence_score,
    processing_time=processing_time
)
    
    embedding = EmbeddingManager.generate_embedding(
    translated_output
)

    FAISSManager.add_embedding(
    embedding,
    translated_output
)

    return TranslationResponse(
        original_text=translation_request.text,
        translated_text=translated_output,
        refined_translation=refined_translation,
        transliterated_text=transliterated_text,
        detected_language=detected_language,
        confidence_score=confidence_score,
        retrieved_contexts=retrieved_contexts,
        semantic_context=semantic_context,
        target_language=translation_request.target_language,
        processing_time=processing_time
    )