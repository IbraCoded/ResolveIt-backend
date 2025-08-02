from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///resolveit.db")
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()