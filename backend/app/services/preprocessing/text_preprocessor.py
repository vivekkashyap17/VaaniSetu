import re
import unicodedata


class TextPreprocessor:


    def normalize_unicode(self, text: str) -> str:

        return unicodedata.normalize("NFKC", text)


    def normalize_whitespace(self, text: str) -> str:

        return " ".join(text.split())


    def lowercase_text(self, text: str) -> str:

        return text.lower()


    def remove_extra_repeated_characters(self, text: str) -> str:

        pattern = r"(.)\1{2,}"

        return re.sub(pattern, r"\1\1", text)


    def preprocess(self, text: str) -> str:

        text = self.normalize_unicode(text)

        text = self.normalize_whitespace(text)

        text = self.lowercase_text(text)

        text = self.remove_extra_repeated_characters(text)

        return text