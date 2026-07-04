# Single source of truth: friendly language name -> NLLB (FLORES-200) code.
# Grouped for readability; the frontend mirrors this list.
SUPPORTED_LANGUAGES = {
    # Global languages
    "english": "eng_Latn",
    "french": "fra_Latn",
    "spanish": "spa_Latn",
    "german": "deu_Latn",
    "arabic": "arb_Arab",
    "chinese": "zho_Hans",
    "russian": "rus_Cyrl",

    # Major Indian languages
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
    "odia": "ory_Orya",
    "assamese": "asm_Beng",
    "nepali": "npi_Deva",
    "sanskrit": "san_Deva",
    "konkani": "gom_Deva",
    "sindhi": "snd_Arab",
    "kashmiri": "kas_Arab",
    "manipuri": "mni_Beng",
    "santali": "sat_Olck",

    # Regional dialects / low-resource languages
    "bhojpuri": "bho_Deva",
    "awadhi": "awa_Deva",
    "maithili": "mai_Deva",
    "magahi": "mag_Deva",
    "chhattisgarhi": "hne_Deva",
}


class LanguageMapper:


    def __init__(self):

        # Detected-language label (rule-based label or langdetect ISO code)
        # -> NLLB source code. Friendly names resolve via SUPPORTED_LANGUAGES;
        # this map only covers detector labels and ISO codes that differ.
        self.language_map = dict(SUPPORTED_LANGUAGES)

        self.language_map.update(
            {
                "roman_hindi": "hin_Deva",
                "en": "eng_Latn",
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
                "or": "ory_Orya",
                "as": "asm_Beng",
                "ne": "npi_Deva",
                "sa": "san_Deva",
                "fr": "fra_Latn",
                "es": "spa_Latn",
                "de": "deu_Latn",
                "ar": "arb_Arab",
                "ru": "rus_Cyrl",
                "zh-cn": "zho_Hans",
                "zh": "zho_Hans",
            }
        )

        # Friendly target-language name (from the request) -> NLLB target code.
        self.target_language_map = dict(SUPPORTED_LANGUAGES)

        # Friendly source-language name (from the request) -> NLLB source code.
        self.source_language_map = dict(SUPPORTED_LANGUAGES)


    def get_language_code(
        self,
        language: str
    ) -> str:

        return self.language_map.get(
            language,
            "eng_Latn"
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


    def get_source_code(
        self,
        source_language: str
    ) -> str:

        key = source_language.lower().strip()

        return self.source_language_map.get(
            key,
            "eng_Latn"
        )
