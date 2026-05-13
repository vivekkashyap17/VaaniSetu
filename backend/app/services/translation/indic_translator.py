from transformers import pipeline


class IndicTranslator:


    def __init__(self):

        self.translator_pipeline = pipeline(
            task="translation",
            model="facebook/nllb-200-distilled-600M"
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