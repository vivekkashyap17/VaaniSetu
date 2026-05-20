from app.db.database import SessionLocal

from app.db.models.translation_record import TranslationRecord


class TranslationRepository:


    @staticmethod
    def save_translation(
        original_text: str,
        translated_text: str,
        detected_language: str,
        confidence_score: float,
        processing_time: float
    ):

        db = SessionLocal()


        translation_record = TranslationRecord(

            original_text=original_text,

            translated_text=translated_text,

            detected_language=detected_language,

            confidence_score=confidence_score,

            processing_time=processing_time
        )


        db.add(translation_record)

        db.commit()

        db.close()