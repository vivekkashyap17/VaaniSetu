from langdetect import detect


class LanguageDetector:


    def is_devanagari(self, text: str) -> bool:

        for char in text:

            if '\u0900' <= char <= '\u097F':
                return True

        return False


    def detect_language(self, text: str) -> str:

        if self.is_devanagari(text):
            return "hindi"

        try:

            detected_language = detect(text)

            return detected_language

        except Exception:

            return "unknown"