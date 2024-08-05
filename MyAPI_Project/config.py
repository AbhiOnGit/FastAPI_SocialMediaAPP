from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # model_config = SettingsConfigDict(env_file=".env")
    class Config:
        # env_file = "D:\\Python_API_VSCode\\MyAPI_Project\\.env"
        env_file = "D:\\Python_API_VSCode\\.env"

setting = Settings()