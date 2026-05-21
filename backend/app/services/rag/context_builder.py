class ContextBuilder:


    def build_translation_context(
        self,
        retrieved_contexts
    ) -> str:

        if not retrieved_contexts:

            return ""


        context = "\n".join(
            retrieved_contexts
        )

        return context