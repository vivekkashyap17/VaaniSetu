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



@router.post(
    "/translate",
    response_model=TranslationResponse
)
async def translate_text(request: TranslationRequest):

    start_time = time.time()

    logger.info("Translation request received")

    pipeline = TranslationPipeline()

    pipeline_output = pipeline.run(request.text)

    processed_text = pipeline_output["processed_text"]

    detected_language = pipeline_output["detected_language"]

    transliterated_text = pipeline_output["transliterated_text"]

    translated_output = pipeline_output["translated_text"]

    processing_time = round(time.time() - start_time, 4)

    return TranslationResponse(
        original_text=request.text,
        translated_text=translated_output,
        transliterated_text=transliterated_text,
        detected_language=detected_language,
        target_language=request.target_language,
        processing_time=processing_time
    )