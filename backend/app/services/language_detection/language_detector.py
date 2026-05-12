from langdetect import detect, detect_langs


class LanguageDetector:


    def __init__(self):

        self.roman_hindi_keywords = {
            "mera",
            "naam",
            "kya",
            "hai",
            "kaise",
            "nahi",
            "haan",
            "acha",
            "tum",
            "hum",
            "bhai",
            "kal",
            "kaha",
            "kyu",
            "kaun",
            "kitna",
            "sab",
            "theek",
            "ho",
            "raha",
            "jana",
            "aaj"
        }

        self.english_keywords = {
            "how",
            "are",
            "you",
            "today",
            "hello",
            "what",
            "where",
            "when",
            "good",
            "morning",
            "night",
            "thanks"
        }


    def is_devanagari(self, text: str) -> bool:

        for char in text:

            if '\u0900' <= char <= '\u097F':
                return True

        return False


    def detect_roman_hindi(self, text: str) -> bool:

        words = set(text.lower().split())

        matched_words = words.intersection(
            self.roman_hindi_keywords
        )

        return len(matched_words) >= 2


    def detect_english(self, text: str) -> bool:

        words = set(text.lower().split())

        matched_words = words.intersection(
            self.english_keywords
        )

        return len(matched_words) >= 2


    def detect_language(self, text: str) -> str:

        if self.is_devanagari(text):
            return "hindi"


        if self.detect_roman_hindi(text):
            return "roman_hindi"


        if self.detect_english(text):
            return "en"


        try:

            predictions = detect_langs(text)

            top_prediction = predictions[0]

            if top_prediction.prob < 0.80:
                return "unknown"

            return top_prediction.lang

        except Exception:

            return "unknown"