from app.services.translation.indic_translator import IndicTranslator

from app.services.translation.indictrans2_translator import IndicTrans2Translator


# NLLB source codes considered "Indic" for engine routing.
INDIC_LANGUAGE_CODES = {
    "hin_Deva",
    "ben_Beng",
    "tam_Taml",
    "tel_Telu",
    "mar_Deva",
    "guj_Gujr",
    "pan_Guru",
    "kan_Knda",
    "mal_Mlym",
    "urd_Arab",
}


class TranslationRouter:
    """Selects a translation engine per (source, target) language pair.

    IndicTrans2 handles Indic-source -> English (better quality on Indian
    languages); NLLB handles everything else (any-to-any fallback).
    Both engines expose the same translate(text, src_lang, tgt_lang) API.
    """


    def __init__(self):

        self.nllb_translator = IndicTranslator()

        self.indictrans2_translator = IndicTrans2Translator()


    def select_engine(
        self,
        src_lang: str,
        tgt_lang: str
    ):

        if src_lang in INDIC_LANGUAGE_CODES and tgt_lang == "eng_Latn":

            return self.indictrans2_translator

        return self.nllb_translator


    def translate(
        self,
        text: str,
        src_lang: str = "hin_Deva",
        tgt_lang: str = "eng_Latn"
    ) -> str:

        engine = self.select_engine(src_lang, tgt_lang)

        return engine.translate(
            text,
            src_lang=src_lang,
            tgt_lang=tgt_lang
        )
