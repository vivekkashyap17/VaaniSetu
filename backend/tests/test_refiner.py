"""LLM refinement fallback guard (regression for blank-on-Indic output).

The refinement model is mocked with a fake callable that mimics the
transformers pipeline return shape, so no model is loaded.
"""

from app.services.llm.translation_refiner import TranslationRefiner


class _FakePipeline:
    """Stand-in for the transformers text2text pipeline object."""

    def __init__(self, generated_text):
        self._generated_text = generated_text

    def __call__(self, prompt, max_new_tokens=64):
        return [{"generated_text": self._generated_text}]


def test_blank_output_falls_back_to_translated_text(monkeypatch):
    monkeypatch.setattr(
        TranslationRefiner, "refinement_pipeline", _FakePipeline("    ")
    )
    result = TranslationRefiner.refine_translation(
        translated_text="My name is Vivek",
        semantic_context="",
    )
    assert result == "My name is Vivek"


def test_nonblank_output_is_returned(monkeypatch):
    monkeypatch.setattr(
        TranslationRefiner, "refinement_pipeline", _FakePipeline("An improved sentence")
    )
    result = TranslationRefiner.refine_translation(
        translated_text="A sentence",
        semantic_context="some context",
    )
    assert result == "An improved sentence"
