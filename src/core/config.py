from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URL: str
    DB_USER: str
    DB_PASSWORD: str
    DB_DATABASE: str
    DB_HOST: str

    APP_NAME: str = "Weather App"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = True

    class Config:
        env_file = ".env"

settings : Settings = Settings()
