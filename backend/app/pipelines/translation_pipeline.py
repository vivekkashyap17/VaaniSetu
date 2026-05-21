from app.services.preprocessing.text_preprocessor import TextPreprocessor

from app.services.language_detection.language_detector import LanguageDetector

from app.services.transliteration.transliterator import Transliterator

from app.services.translation.indic_translator import IndicTranslator

from app.services.language_detection.language_mapper import LanguageMapper

from app.core.cache.cache_manager import CacheManager

from app.services.evaluation.quality_evaluator import QualityEvaluator

from app.services.rag.retrieval_service import RetrievalService

from app.services.rag.context_builder import ContextBuilder


class TranslationPipeline:


    def __init__(self):

        self.preprocessor = TextPreprocessor()

        self.language_detector = LanguageDetector()

        self.transliterator = Transliterator()

        self.translator = IndicTranslator()

        self.language_mapper = LanguageMapper()

        self.quality_evaluator = QualityEvaluator()

        self.retrieval_service = RetrievalService()

        self.context_builder = ContextBuilder()


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

        retrieved_contexts = (
    self.retrieval_service.retrieve_similar_contexts(
        transliterated_text
    )
)

        semantic_context = (
    self.context_builder.build_translation_context(
        retrieved_contexts
    )
)

        cache_key = CacheManager.generate_cache_key(
            transliterated_text,
            "english"
        )

        cached_translation = (
            CacheManager.get_cached_translation(
                cache_key
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

            cache_hit = False


            if cached_translation:
                cache_hit = True

                print("Cache hit")

                translated_text = cached_translation

            else:

                print("Running model inference")

                translated_text = self.translator.translate(
                    transliterated_text,
                    src_lang=source_language_code,
                    tgt_lang=target_language_code
                )

                CacheManager.store_translation(
                    cache_key,
                    translated_text
                )
        confidence_score = (
    self.quality_evaluator.evaluate_translation_confidence(
        transliterated_text,
        translated_text
    )
)
        

        return {
            "processed_text": processed_text,
            "detected_language": detected_language,
            "transliterated_text": transliterated_text,
            "translated_text": translated_text,
            "confidence_score": confidence_score,
            "cache_hit": cache_hit,
            "retrieved_contexts": retrieved_contexts,
            "semantic_context": semantic_context
        }