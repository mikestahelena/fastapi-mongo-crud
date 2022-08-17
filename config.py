from pydantic import BaseSettings


class CommonSettings(BaseSettings):
    APP_NAME: str = "FastAPI+MongoDB basic CRUD"
    DEBUG_MODE: bool = True


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    DB_USERNAME: str = ""
    DB_PASS: str = ""
    DB_NAME: str = ""
    DB_HOST: str = ""
    DB_URL: str = (
        f"mongodb+srv://{DB_USERNAME}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    )


class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()
