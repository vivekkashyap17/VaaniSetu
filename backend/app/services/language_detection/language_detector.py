from langdetect import detect_langs


# Unicode script ranges -> detected friendly label. Ordered by script block.
SCRIPT_RANGES = [
    ("bengali", 0x0980, 0x09FF),
    ("punjabi", 0x0A00, 0x0A7F),
    ("gujarati", 0x0A80, 0x0AFF),
    ("odia", 0x0B00, 0x0B7F),
    ("tamil", 0x0B80, 0x0BFF),
    ("telugu", 0x0C00, 0x0C7F),
    ("kannada", 0x0C80, 0x0CFF),
    ("malayalam", 0x0D00, 0x0D7F),
    ("urdu", 0x0600, 0x06FF),
    ("hindi", 0x0900, 0x097F),
]


# langdetect ISO codes we trust as a fallback for latin/other scripts.
SUPPORTED_ISO = {
    "en",
    "fr",
    "es",
    "de",
    "ru",
    "ar",
    "zh-cn",
    "zh",
}


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


    def detect_script(self, text: str) -> str:

        # Devanagari is checked last so more specific Indic scripts win first,
        # but any single matching character settles the script.
        for char in text:

            code_point = ord(char)

            for label, low, high in SCRIPT_RANGES:

                if low <= code_point <= high:
                    return label

        return ""


    def detect_roman_hindi(self, text: str) -> bool:

        words = set(text.lower().split())

        matched_words = words.intersection(
            self.roman_hindi_keywords
        )

        return len(matched_words) >= 2


    def detect_language(self, text: str) -> str:

        script_label = self.detect_script(text)

        if script_label:
            return script_label


        if self.detect_roman_hindi(text):
            return "roman_hindi"


        try:

            predictions = detect_langs(text)

            top_prediction = predictions[0]

            if top_prediction.prob < 0.80:
                return "en"

            if top_prediction.lang not in SUPPORTED_ISO:
                return "en"

            return top_prediction.lang

        except Exception:

            return "en"
