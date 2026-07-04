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

    def test_tamil_script_detected(self):
        assert self.detector.detect_language("என் பெயர் விவேக்") == "tamil"

    def test_telugu_script_detected(self):
        assert self.detector.detect_language("నా పేరు వివేక్") == "telugu"

    def test_gujarati_script_detected(self):
        assert self.detector.detect_language("મારું નામ વિવેક છે") == "gujarati"

    def test_gurmukhi_script_detected_as_punjabi(self):
        assert self.detector.detect_language("ਮੇਰਾ ਨਾਮ ਵਿਵੇਕ ਹੈ") == "punjabi"

    def test_kannada_script_detected(self):
        assert self.detector.detect_language("ನನ್ನ ಹೆಸರು ವಿವೇಕ್") == "kannada"

    def test_malayalam_script_detected(self):
        assert self.detector.detect_language("എന്റെ പേര് വിവേക്") == "malayalam"

    def test_odia_script_detected(self):
        assert self.detector.detect_language("ମୋର ନାମ ବିବେକ") == "odia"

    def test_roman_hindi_keywords(self):
        # >= 2 roman-Hindi keyword matches (mera, naam, kya, hai)
        assert self.detector.detect_language("mera naam kya hai") == "roman_hindi"

    def test_english_falls_through_to_langdetect(self):
        assert self.detector.detect_language("how are you today") == "en"

    def test_langdetect_fallback_for_other_language(self):
        # No script/keyword rule fires -> langdetect fallback
        assert self.detector.detect_language("bonjour comment allez vous") == "fr"

    def test_undetectable_input_falls_back_to_english(self):
        # No script/keyword/langdetect signal -> safe latin default (english)
        assert self.detector.detect_language("123 456 789") == "en"


class TestLanguageMapper:

    def setup_method(self):
        self.mapper = LanguageMapper()

    def test_known_codes(self):
        assert self.mapper.get_language_code("hindi") == "hin_Deva"
        assert self.mapper.get_language_code("tamil") == "tam_Taml"
        assert self.mapper.get_language_code("en") == "eng_Latn"

    def test_roman_hindi_maps_to_devanagari(self):
        assert self.mapper.get_language_code("roman_hindi") == "hin_Deva"

    def test_unknown_language_defaults_to_english(self):
        assert self.mapper.get_language_code("klingon") == "eng_Latn"

    def test_langdetect_iso_codes_map_to_nllb(self):
        assert self.mapper.get_language_code("fr") == "fra_Latn"
        assert self.mapper.get_language_code("ta") == "tam_Taml"

    def test_dialect_and_extended_language_codes(self):
        assert self.mapper.get_target_code("bhojpuri") == "bho_Deva"
        assert self.mapper.get_target_code("awadhi") == "awa_Deva"
        assert self.mapper.get_target_code("maithili") == "mai_Deva"
        assert self.mapper.get_target_code("chhattisgarhi") == "hne_Deva"
        assert self.mapper.get_target_code("odia") == "ory_Orya"
        assert self.mapper.get_target_code("assamese") == "asm_Beng"
        assert self.mapper.get_target_code("sanskrit") == "san_Deva"

    def test_target_code_known_names(self):
        assert self.mapper.get_target_code("english") == "eng_Latn"
        assert self.mapper.get_target_code("tamil") == "tam_Taml"
        assert self.mapper.get_target_code("french") == "fra_Latn"

    def test_target_code_is_case_and_space_insensitive(self):
        assert self.mapper.get_target_code("  English ") == "eng_Latn"
        assert self.mapper.get_target_code("TAMIL") == "tam_Taml"

    def test_target_code_unknown_defaults_to_english(self):
        assert self.mapper.get_target_code("klingon") == "eng_Latn"

    def test_source_code_known_names(self):
        assert self.mapper.get_source_code("hindi") == "hin_Deva"
        assert self.mapper.get_source_code("  Bhojpuri ") == "bho_Deva"

    def test_source_code_unknown_defaults_to_english(self):
        assert self.mapper.get_source_code("klingon") == "eng_Latn"
