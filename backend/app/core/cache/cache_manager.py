class CacheManager:


    translation_cache = {}


    @classmethod
    def generate_cache_key(
        cls,
        text: str,
        target_language: str
    ) -> str:

        return f"{text}:{target_language}"


    @classmethod
    def get_cached_translation(
        cls,
        cache_key: str
    ):

        return cls.translation_cache.get(cache_key)


    @classmethod
    def store_translation(
        cls,
        cache_key: str,
        translated_text: str
    ):

        cls.translation_cache[cache_key] = translated_text