from pydantic_settings import BaseSettings
from pydantic import ConfigDict
class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str ="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES:int = 15
    REFRESH_TOKEN_EXPIRE_DAYS:int = 30
    DATABASE_URL: str
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
