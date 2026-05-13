from transformers import pipeline


class ModelManager:


    translator_pipeline = None


    @classmethod
    def load_models(cls):

        if cls.translator_pipeline is None:

            print("Loading translation model...")

            cls.translator_pipeline = pipeline(
                task="translation",
                model="facebook/nllb-200-distilled-600M"
            )

            print("Translation model loaded.")


    @classmethod
    def get_translation_pipeline(cls):

        return cls.translator_pipeline