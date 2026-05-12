from transformers import pipeline


class Translator:

    def __init__(self):

        self.translator_pipeline = pipeline(
            task="translation",
            model="Helsinki-NLP/opus-mt-hi-en"
        )

    def translate(
        self,
        text: str
    ) -> str:

        output = self.translator_pipeline(text)

        translated_text = output[0]["translation_text"]

        return translated_text