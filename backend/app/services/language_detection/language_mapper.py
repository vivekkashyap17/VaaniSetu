class LanguageMapper:


    def __init__(self):

        self.language_map = {

            "hindi": "hin_Deva",

            "roman_hindi": "hin_Deva",

            "en": "eng_Latn",

            "bengali": "ben_Beng",

            "tamil": "tam_Taml",

            "telugu": "tel_Telu",

            "marathi": "mar_Deva",

            "gujarati": "guj_Gujr",

            "punjabi": "pan_Guru"
        }


    def get_language_code(
        self,
        language: str
    ) -> str:

        return self.language_map.get(
            language,
            "hin_Deva"
        )