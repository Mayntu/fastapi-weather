from fastapi import Depends

from src.repositories import WeatherRepository, get_weather_repo
from src.services import WeatherService, WeatherFetcher

import httpx

_client: httpx.AsyncClient | None = None

async def get_http_client() -> httpx.AsyncClient:
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(timeout=10)
    return _client


def get_weather_fetcher(http_client : httpx.AsyncClient = Depends(get_http_client)) -> WeatherFetcher:
    return WeatherFetcher(client=http_client)


def get_weather_service(
        repo: WeatherRepository = Depends(get_weather_repo),
        weather_fetcher: WeatherFetcher = Depends(get_weather_fetcher)
    ) -> WeatherService:
    return WeatherService(repo, weather_fetcher)