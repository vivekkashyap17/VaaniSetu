from transformers import pipeline


class TranslationRefiner:


    refinement_pipeline = None


    @classmethod
    def load_refinement_model(cls):

        if cls.refinement_pipeline is None:

            print("Loading LLM refinement model...")

            cls.refinement_pipeline = pipeline(
                task="text2text-generation",
                model="google/flan-t5-base"
            )

            print("LLM refinement model loaded.")


    @classmethod
    def refine_translation(
        cls,
        original_text: str,
        translated_text: str,
        semantic_context: str
    ) -> str:

        prompt = f"""
        Improve the following translation.

        Original Text:
        {original_text}

        Initial Translation:
        {translated_text}

        Semantic Context:
        {semantic_context}

        Return only the improved translation.
        """


        result = cls.refinement_pipeline(
            prompt,
            max_new_tokens=64
        )


        refined_text = result[0]["generated_text"]

        return refined_text