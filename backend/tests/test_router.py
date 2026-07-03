"""Engine routing: IndicTrans2 for Indic->English, NLLB for everything else.

select_engine() is pure logic; constructing the router does not load models.
"""

from app.services.translation.translation_router import TranslationRouter
from app.services.translation.indic_translator import IndicTranslator
from app.services.translation.indictrans2_translator import IndicTrans2Translator


class TestTranslationRouter:

    def setup_method(self):
        self.router = TranslationRouter()

    def test_indic_to_english_uses_indictrans2(self):
        engine = self.router.select_engine("hin_Deva", "eng_Latn")
        assert isinstance(engine, IndicTrans2Translator)

    def test_tamil_to_english_uses_indictrans2(self):
        engine = self.router.select_engine("tam_Taml", "eng_Latn")
        assert isinstance(engine, IndicTrans2Translator)

    def test_indic_to_indic_uses_nllb(self):
        engine = self.router.select_engine("hin_Deva", "tam_Taml")
        assert isinstance(engine, IndicTranslator)

    def test_english_to_indic_uses_nllb(self):
        engine = self.router.select_engine("eng_Latn", "tam_Taml")
        assert isinstance(engine, IndicTranslator)

    def test_non_indic_to_english_uses_nllb(self):
        engine = self.router.select_engine("fra_Latn", "eng_Latn")
        assert isinstance(engine, IndicTranslator)
