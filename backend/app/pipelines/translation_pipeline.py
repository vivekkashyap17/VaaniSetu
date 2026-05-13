from app.services.preprocessing.text_preprocessor import TextPreprocessor

from app.services.language_detection.language_detector import LanguageDetector

from app.services.transliteration.transliterator import Transliterator

from app.services.translation.indic_translator import IndicTranslator

from app.services.language_detection.language_mapper import LanguageMapper


class TranslationPipeline:


    def __init__(self):

        self.preprocessor = TextPreprocessor()

        self.language_detector = LanguageDetector()

        self.transliterator = Transliterator()

        self.translator = IndicTranslator()

        self.language_mapper = LanguageMapper()


    def run(self, text: str):

        processed_text = self.preprocessor.preprocess(text)

        detected_language = self.language_detector.detect_language(
            processed_text
        )

        transliterated_text = processed_text


        if detected_language == "roman_hindi":

            transliterated_text = (
                self.transliterator.transliterate_roman_hindi(
                    processed_text
                )
            )


        translated_text = transliterated_text


        source_language_code = (
            self.language_mapper.get_language_code(
                detected_language
            )
        )

        target_language_code = (
            self.language_mapper.get_language_code(
                "en"
            )
        )


        if detected_language in [
            "hindi",
            "roman_hindi",
            "bengali",
            "tamil",
            "telugu",
            "marathi",
            "gujarati",
            "punjabi"
        ]:

            translated_text = self.translator.translate(
                transliterated_text,
                src_lang=source_language_code,
                tgt_lang=target_language_code
            )


        return {
            "processed_text": processed_text,
            "detected_language": detected_language,
            "transliterated_text": transliterated_text,
            "translated_text": translated_text
        }