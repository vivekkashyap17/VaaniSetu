from app.core.config.settings import get_settings

settings = get_settings()


class IndicTrans2Manager:


    tokenizer = None

    model = None

    processor = None


    @classmethod
    def load(cls):

        if cls.model is None:

            print("Loading IndicTrans2 indic-en model...")

            from transformers import AutoModelForSeq2SeqLM
            from transformers import AutoTokenizer

            from IndicTransToolkit.processor import IndicProcessor

            model_name = settings.INDICTRANS2_INDIC_EN_MODEL

            cls.tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                trust_remote_code=True
            )

            cls.model = AutoModelForSeq2SeqLM.from_pretrained(
                model_name,
                trust_remote_code=True
            )

            cls.processor = IndicProcessor(inference=True)

            print("IndicTrans2 indic-en model loaded.")
