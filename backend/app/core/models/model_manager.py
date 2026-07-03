from transformers import pipeline

from app.core.config.settings import get_settings

settings = get_settings()


class ModelManager:


    translator_pipeline = None


    @classmethod
    def load_models(cls):

        if cls.translator_pipeline is None:

            print("Loading translation model...")

            cls.translator_pipeline = pipeline(
                task="translation",
                model=settings.TRANSLATION_MODEL
            )

            print("Translation model loaded.")


    @classmethod
    def get_translation_pipeline(cls):

        return cls.translator_pipeline