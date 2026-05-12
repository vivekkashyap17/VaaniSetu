import time

from fastapi import APIRouter

from app.core.logging.logger import setup_logger

from app.schemas.translation import (
    TranslationRequest,
    TranslationResponse
)

from app.pipelines.translation_pipeline import TranslationPipeline


router = APIRouter()

logger = setup_logger()

pipeline = TranslationPipeline()


@router.post(
    "/translate",
    response_model=TranslationResponse
)
async def translate_text(request: TranslationRequest):

    start_time = time.time()

    logger.info("Translation request received")

    processed_text = pipeline.run(request.text)

    translated_output = f"Translated: {processed_text}"

    processing_time = round(time.time() - start_time, 4)

    return TranslationResponse(
        original_text=request.text,
        translated_text=translated_output,
        detected_language=request.source_language,
        target_language=request.target_language,
        processing_time=processing_time
    )