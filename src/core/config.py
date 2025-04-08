
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    BIGQUERY_SERVICE_ACCOUNT_JSON: str
    REDIS_SERVER_URL: str

    class Config:
        env_file = ""

@lru_cache
def get_settings():
    return Settings()
