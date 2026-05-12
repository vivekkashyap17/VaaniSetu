from app.services.preprocessing.text_preprocessor import TextPreprocessor

from app.services.language_detection.language_detector import LanguageDetector


class TranslationPipeline:


    def __init__(self):

        self.preprocessor = TextPreprocessor()

        self.language_detector = LanguageDetector()


    def run(self, text: str):

        processed_text = self.preprocessor.preprocess(text)

        detected_language = self.language_detector.detect_language(
            processed_text
        )

        return {
            "processed_text": processed_text,
            "detected_language": detected_language
        }