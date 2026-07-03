"""Pure-logic pipeline helpers: cache, preprocessing, quality, context."""

from app.core.cache.cache_manager import CacheManager
from app.services.preprocessing.text_preprocessor import TextPreprocessor
from app.services.evaluation.quality_evaluator import QualityEvaluator
from app.services.rag.context_builder import ContextBuilder


class TestCacheManager:

    def test_generate_cache_key(self):
        assert CacheManager.generate_cache_key("hello", "english") == "hello:english"

    def test_store_and_get_roundtrip(self):
        key = CacheManager.generate_cache_key("unit-test-store", "english")
        CacheManager.store_translation(key, "translated value")
        assert CacheManager.get_cached_translation(key) == "translated value"

    def test_missing_key_returns_none(self):
        assert CacheManager.get_cached_translation("unit-test-missing:english") is None


class TestTextPreprocessor:

    def setup_method(self):
        self.pre = TextPreprocessor()

    def test_collapses_whitespace(self):
        assert self.pre.normalize_whitespace("a   b\n c") == "a b c"

    def test_lowercases(self):
        assert self.pre.lowercase_text("HeLLo") == "hello"

    def test_repeated_characters_capped_at_two(self):
        assert self.pre.remove_extra_repeated_characters("soooo") == "soo"

    def test_preprocess_full_chain(self):
        # "Cooool" -> lowercase + collapse 4 o's down to 2 -> "cool"
        assert self.pre.preprocess("Cooool") == "cool"

    def test_preprocess_trims_and_lowercases(self):
        assert self.pre.preprocess("  Hello    WORLD  ") == "hello world"


class TestQualityEvaluator:

    def setup_method(self):
        self.qe = QualityEvaluator()

    def test_similar_length_high_confidence(self):
        assert self.qe.evaluate_translation_confidence("a b c", "d e f") == 0.95

    def test_empty_translation_zero_confidence(self):
        assert self.qe.evaluate_translation_confidence("a b c", "") == 0.0

    def test_moderate_length_ratio_medium_confidence(self):
        # 5 words -> 2 words = ratio 0.4 (in [0.3, 0.5))
        assert self.qe.evaluate_translation_confidence("a b c d e", "x y") == 0.75

    def test_extreme_length_ratio_low_confidence(self):
        # 1 word -> 3 words = ratio 3.0 (> 2.0)
        assert self.qe.evaluate_translation_confidence("a", "x y z") == 0.50


class TestContextBuilder:

    def setup_method(self):
        self.cb = ContextBuilder()

    def test_empty_contexts_returns_empty_string(self):
        assert self.cb.build_translation_context([]) == ""

    def test_joins_contexts_with_newline(self):
        assert self.cb.build_translation_context(["one", "two"]) == "one\ntwo"
