"""Shared pytest setup.

Set required config env vars BEFORE any app module is imported, so the
pydantic-settings `Settings` (all fields required, no defaults) loads
deterministically without depending on a local .env file. These override
.env because real environment variables take priority in pydantic-settings.
"""

import os

_TEST_ENV = {
    "APP_NAME": "BhashaBridge-Test",
    "APP_VERSION": "0.0.0",
    "DEBUG": "true",
    "HOST": "127.0.0.1",
    "PORT": "8000",
    "PROJECT_NAME": "BhashaBridge",
    "API_KEY": "test-secret-key",
    "DATABASE_URL": "sqlite:///./test_bhashabridge.db",
    "TRANSLATION_MODEL": "facebook/nllb-200-distilled-600M",
    "EMBEDDING_MODEL": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    "REFINEMENT_MODEL": "google/flan-t5-base",
    "INDICTRANS2_INDIC_EN_MODEL": "ai4bharat/indictrans2-indic-en-dist-200M",
    "RATE_LIMIT": "5/minute",
}

for _key, _value in _TEST_ENV.items():
    os.environ[_key] = _value
