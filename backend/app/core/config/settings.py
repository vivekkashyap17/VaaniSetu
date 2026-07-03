from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    APP_NAME: str

    APP_VERSION: str

    DEBUG: bool

    HOST: str

    PORT: int

    PROJECT_NAME: str

    API_KEY: str

    DATABASE_URL: str

    TRANSLATION_MODEL: str

    EMBEDDING_MODEL: str

    REFINEMENT_MODEL: str

    RATE_LIMIT: str

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():

    return Settings()