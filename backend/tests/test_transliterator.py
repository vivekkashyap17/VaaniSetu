"""Roman-Hindi -> Devanagari transliteration."""

from app.services.transliteration.transliterator import Transliterator


def _has_devanagari(text: str) -> bool:
    return any("ऀ" <= ch <= "ॿ" for ch in text)


class TestTransliterator:

    def setup_method(self):
        self.transliterator = Transliterator()

    def test_roman_hindi_produces_devanagari(self):
        result = self.transliterator.transliterate_roman_hindi("mera naam")
        assert isinstance(result, str)
        assert _has_devanagari(result)

    def test_output_differs_from_ascii_input(self):
        text = "namaste"
        result = self.transliterator.transliterate_roman_hindi(text)
        assert result != text
