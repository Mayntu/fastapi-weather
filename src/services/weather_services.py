from uuid import UUID

from loguru import logger as log

from src.models import Weather
from src.repositories import WeatherRepository
from src.services.weather_fetcher import WeatherFetcher
from src.schemas import WeatherRead, WeatherUpdate, WeatherCreate
from src.exceptions import WeatherNotFoundException


class WeatherService:
    def __init__(self, repo : WeatherRepository, weather_fetcher : WeatherFetcher):
        self.repo = repo
        self.fetcher = weather_fetcher

    async def get_by_id(self, id: UUID) -> WeatherRead:
        weather : Weather = await self.repo.get(id)
        if not weather:
            raise WeatherNotFoundException()
        
        return WeatherRead.model_validate(weather)
    
    async def get_latest_by_city(self, city : str) -> WeatherRead:
        weather : Weather = await self.repo.get_latest_by_city(city)
        if not weather:
            raise WeatherNotFoundException()
        
        return WeatherRead.model_validate(weather)
    
    async def get_latest_all(self) -> list[WeatherRead]:
        result : list[WeatherRead] = await self.repo.get_latest_for_all_cities()
        return result

    async def delete(self, id : UUID) -> None:
        weather : Weather = await self.repo.get(id)
        if not weather:
            raise WeatherNotFoundException()
        
        await self.repo.delete(weather)
    
    async def refresh_city(self, city: str, country: str):
        data = await self.fetcher.fetch(city, country)

        existing = await self.repo.many(city=city)

        if existing:
            weather = existing[0]
            return await self.repo.update(
                weather_to_update=weather,
                weather_new_data=WeatherUpdate(
                    temperature=data["temperature"],
                    humidity=data["humidity"],
                    pressure=data["pressure"],
                    fetched_at=data["fetched_at"],
                ),
            )

        weather_created : Weather = await self.repo.create(WeatherCreate(**data))
        return WeatherRead.model_validate(weather_created)
