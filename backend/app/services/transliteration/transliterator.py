from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate


class Transliterator:


    def transliterate_roman_hindi(
        self,
        text: str
    ) -> str:

        transliterated_text = transliterate(
            text,
            sanscript.ITRANS,
            sanscript.DEVANAGARI
        )

        return transliterated_text