import os
from dotenv import load_dotenv

from pydantic import BaseSettings

load_dotenv()


class CommonSettings(BaseSettings):
    APP_NAME: str = "FastAPI+MongoDB basic CRUD"
    DEBUG_MODE: bool = True


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    DB_USERNAME: str = os.getenv("MONGO_INITDB_ROOT_USERNAME")
    DB_PASS: str = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
    DB_NAME: str = os.getenv("MONGO_INITDB_DATABASE")
    DB_HOST: str = os.getenv("MONGO_INITDB_HOST")
    DB_URL: str = f"mongodb://{DB_USERNAME}:{DB_PASS}@{DB_HOST}:27017/{DB_NAME}?" \
                  "authSource=admin&readPreference=secondary&directConnection=true&ssl=false"


class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()
