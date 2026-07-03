"""Language detection and language-code mapping."""

from app.services.language_detection.language_detector import LanguageDetector
from app.services.language_detection.language_mapper import LanguageMapper


class TestLanguageDetector:

    def setup_method(self):
        self.detector = LanguageDetector()

    def test_devanagari_detected_as_hindi(self):
        assert self.detector.detect_language("मेरा नाम विवेक है") == "hindi"

    def test_bengali_script_detected(self):
        assert self.detector.detect_language("আমার নাম রাহুল") == "bengali"

    def test_roman_hindi_keywords(self):
        # >= 2 roman-Hindi keyword matches (mera, naam, kya, hai)
        assert self.detector.detect_language("mera naam kya hai") == "roman_hindi"

    def test_english_keywords(self):
        # >= 2 english keyword matches (how, are, you, today)
        assert self.detector.detect_language("how are you today") == "en"

    def test_langdetect_fallback_for_other_language(self):
        # No script/keyword rule fires -> langdetect fallback
        assert self.detector.detect_language("bonjour comment allez vous") == "fr"

    def test_unknown_for_undetectable_input(self):
        # langdetect cannot extract features from digits -> "unknown"
        assert self.detector.detect_language("123 456 789") == "unknown"


class TestLanguageMapper:

    def setup_method(self):
        self.mapper = LanguageMapper()

    def test_known_codes(self):
        assert self.mapper.get_language_code("hindi") == "hin_Deva"
        assert self.mapper.get_language_code("tamil") == "tam_Taml"
        assert self.mapper.get_language_code("en") == "eng_Latn"

    def test_roman_hindi_maps_to_devanagari(self):
        assert self.mapper.get_language_code("roman_hindi") == "hin_Deva"

    def test_unknown_language_defaults_to_hindi(self):
        assert self.mapper.get_language_code("klingon") == "hin_Deva"
