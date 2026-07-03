class LanguageMapper:


    def __init__(self):

        # Detected-language label (rule-based label or langdetect ISO code)
        # -> NLLB source code.
        self.language_map = {
            "hindi": "hin_Deva",
            "roman_hindi": "hin_Deva",
            "en": "eng_Latn",
            "bengali": "ben_Beng",
            "tamil": "tam_Taml",
            "telugu": "tel_Telu",
            "marathi": "mar_Deva",
            "gujarati": "guj_Gujr",
            "punjabi": "pan_Guru",
            "hi": "hin_Deva",
            "bn": "ben_Beng",
            "ta": "tam_Taml",
            "te": "tel_Telu",
            "mr": "mar_Deva",
            "gu": "guj_Gujr",
            "pa": "pan_Guru",
            "kn": "kan_Knda",
            "ml": "mal_Mlym",
            "ur": "urd_Arab",
            "fr": "fra_Latn",
            "es": "spa_Latn",
            "de": "deu_Latn",
        }

        # Friendly target-language name (from the request) -> NLLB target code.
        self.target_language_map = {
            "english": "eng_Latn",
            "hindi": "hin_Deva",
            "bengali": "ben_Beng",
            "tamil": "tam_Taml",
            "telugu": "tel_Telu",
            "marathi": "mar_Deva",
            "gujarati": "guj_Gujr",
            "punjabi": "pan_Guru",
            "kannada": "kan_Knda",
            "malayalam": "mal_Mlym",
            "urdu": "urd_Arab",
            "french": "fra_Latn",
            "spanish": "spa_Latn",
            "german": "deu_Latn",
        }


    def get_language_code(
        self,
        language: str
    ) -> str:

        return self.language_map.get(
            language,
            "hin_Deva"
        )


    def get_target_code(
        self,
        target_language: str
    ) -> str:

        key = target_language.lower().strip()

        return self.target_language_map.get(
            key,
            "eng_Latn"
        )
