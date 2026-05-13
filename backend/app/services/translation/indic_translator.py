from app.core.models.model_manager import ModelManager


class IndicTranslator:


    def __init__(self):

        self.translator_pipeline = (
            ModelManager.get_translation_pipeline()
        )


    def translate(
        self,
        text: str,
        src_lang: str = "hin_Deva",
        tgt_lang: str = "eng_Latn"
    ) -> str:

        output = self.translator_pipeline(
            text,
            src_lang=src_lang,
            tgt_lang=tgt_lang
        )

        translated_text = output[0]["translation_text"]

        return translated_text