from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    DB_URL: str
    DB_USER: str
    DB_PASSWORD: str
    DB_DATABASE: str
    DB_HOST: str

    APP_NAME: str = "Weather App"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = True

    WEATHER_API_KEY: str
    WEATHER_API_URL: str = "https://api.weatherapi.com/v1/current.json"

    DEFAULT_CITIES: list[str] = [
        "Almaty,KZ",
        "Astana,KZ",
        "Berlin,DE",
    ]

    model_config = ConfigDict(env_file=".env", extra="ignore")

settings : Settings = Settings()
