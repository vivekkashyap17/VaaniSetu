class QualityEvaluator:


    def evaluate_translation_confidence(
        self,
        original_text: str,
        translated_text: str
    ) -> float:

        original_length = len(original_text.split())

        translated_length = len(translated_text.split())


        if translated_length == 0:
            return 0.0


        length_ratio = (
            translated_length / max(original_length, 1)
        )


        if 0.5 <= length_ratio <= 1.5:
            return 0.95


        if 0.3 <= length_ratio <= 2.0:
            return 0.75


        return 0.50