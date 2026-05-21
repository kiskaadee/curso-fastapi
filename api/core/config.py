from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Platzi FastAPI Course"
    PROJECT_VERSION: str = "1.0.0"
    CORS_ORIGINS: list[str] = ["*"]
    DEBUG_MODE: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
