import torch

from app.core.models.indictrans2_manager import IndicTrans2Manager


class IndicTrans2Translator:
    """AI4Bharat IndicTrans2 engine, used for Indic-source -> English."""


    def translate(
        self,
        text: str,
        src_lang: str = "hin_Deva",
        tgt_lang: str = "eng_Latn"
    ) -> str:

        IndicTrans2Manager.load()

        tokenizer = IndicTrans2Manager.tokenizer

        model = IndicTrans2Manager.model

        processor = IndicTrans2Manager.processor

        batch = processor.preprocess_batch(
            [text],
            src_lang=src_lang,
            tgt_lang=tgt_lang
        )

        inputs = tokenizer(
            batch,
            truncation=True,
            padding="longest",
            return_tensors="pt"
        )

        with torch.no_grad():

            generated = model.generate(
                **inputs,
                use_cache=True,
                min_length=0,
                max_length=256,
                num_beams=5,
                num_return_sequences=1
            )

        decoded = tokenizer.batch_decode(
            generated,
            skip_special_tokens=True
        )

        translations = processor.postprocess_batch(
            decoded,
            lang=tgt_lang
        )

        return translations[0]
