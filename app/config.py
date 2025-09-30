from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# carrega variáveis do arquivo .env
load_dotenv()

class Settings(BaseSettings):
    MONGO_URL: str
    MONGO_DB: str = "chatdb"
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000

    class Config:
        env_file = ".env"

settings = Settings()
