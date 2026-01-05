from uuid import UUID

from src.models import Weather
from src.repositories import WeatherRepository
from src.services.weather_fetcher import WeatherFetcher
from src.schemas import WeatherRead, WeatherUpdate, WeatherCreate

class WeatherNotFoundException(Exception):
    # status_code = 404
    pass

class WeatherService:
    def __init__(self, repo : WeatherRepository, weather_fetcher : WeatherFetcher):
        self.repo = repo
        self.fetcher = weather_fetcher

    async def get_by_id(self, id: UUID) -> WeatherRead:
        weather : Weather = await self.repo.get(id)
        if not weather:
            raise WeatherNotFoundException(detail="Weather Not Found")
        
        return weather
    
    async def get_many(self, city : str) -> list[WeatherRead]:
        result : list[WeatherRead] = await self.repo.many(city=city)
        return result

    async def delete(self, id : UUID) -> None:
        weather : Weather = await self.repo.get(id)
        if not weather:
            raise WeatherNotFoundException(detail="Weather Not Found")
        
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

        return await self.repo.create(WeatherCreate(**data))