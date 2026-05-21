from pydantic import BaseModel, Field


class TranslationRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Input text for translation"
    )

    source_language: str = Field(
        default="auto",
        description="Source language or dialect"
    )

    target_language: str = Field(
        ...,
        description="Target translation language"
    )


class TranslationResponse(BaseModel):

    original_text: str

    translated_text: str

    detected_language: str

    target_language: str

    processing_time: float

    transliterated_text: str

    confidence_score: float

    retrieved_contexts: list
    
    semantic_context: str