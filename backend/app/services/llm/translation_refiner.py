import time

from transformers import pipeline

from app.core.model_management.device_manager import DeviceManager

from app.core.config.settings import get_settings

settings = get_settings()


class TranslationRefiner:


    refinement_pipeline = None


    @classmethod
    def load_refinement_model(cls):

        if cls.refinement_pipeline is None:

            print("Loading LLM refinement model...")

            device = DeviceManager.get_device()

            print(f"Using device: {device}")

            pipeline_device = 0 if device == "cuda" else -1

            cls.refinement_pipeline = pipeline(
                task="text2text-generation",
                model=settings.REFINEMENT_MODEL,
                device=pipeline_device
            )

            print("LLM refinement model loaded.")


    @classmethod
    def refine_translation(
        cls,
        translated_text: str,
        semantic_context: str
    ) -> str:

        prompt = f"""
        Improve the following English translation.

        Translation:
        {translated_text}

        Semantic Context:
        {semantic_context}

        Return only the improved translation.
        """


        start_time = time.time()

        result = cls.refinement_pipeline(
            prompt,
            max_new_tokens=64
        )

        end_time = time.time()

        print(
            f"LLM refinement time: "
            f"{round(end_time - start_time, 2)} seconds"
        )


        refined_text = result[0]["generated_text"]


        if refined_text.strip() == "":

            print("Refinement produced empty output; falling back to translated text")

            return translated_text


        return refined_text