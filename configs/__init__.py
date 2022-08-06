import os
from functools import lru_cache

from pydantic import BaseSettings


def get_env_file():
    stage = os.environ.get('ENV') or 'dev'
    return '.env.{}'.format(stage)


class Settings(BaseSettings):
    APP_NAME: str = "The Endings API"
    DEBUG: bool = False
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    USERPROFILE_DOC_TYPE: str
    DB_DATABASE: str
    DB_URL: str

    class Config:
        env_file = get_env_file()


Configs = Settings()

print('Configs:\n', Configs)


@lru_cache()
def get_settings():
    return Configs
