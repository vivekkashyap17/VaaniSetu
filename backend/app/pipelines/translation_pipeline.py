from app.services.preprocessing.text_preprocessor import TextPreprocessor


class TranslationPipeline:


    def __init__(self):

        self.preprocessor = TextPreprocessor()


    def run(self, text: str):

        processed_text = self.preprocessor.preprocess(text)

        return processed_text