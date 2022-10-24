from pydantic import BaseConfig, SecretStr


class Settings(BaseConfig):

    bot_token: SecretStr

    class Config:
        env_file = ".bot/env"  # source file with token
        env_file_encoding = 'utf-8'


config = Settings()