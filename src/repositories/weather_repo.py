from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Weather
from src.schemas import WeatherCreate, WeatherUpdate


class WeatherRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: WeatherCreate) -> Weather:
        weather : Weather = Weather(**data.model_dump())
        self.session.add(weather)
        await self.session.commit()
        await self.session.refresh(weather)
        return weather

    async def get(self, weather_id) -> Weather | None:
        return await self.session.get(Weather, weather_id)

    async def many(self, city: str | None = None) -> list[Weather]:
        stmt = select(Weather)
        if city:
            stmt = stmt.where(Weather.city == city)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update(
        self, weather_to_update: Weather, weather_new_data: WeatherUpdate
    ) -> Weather:
        for field, value in weather_new_data.model_dump(exclude_unset=True).items():
            setattr(weather_to_update, field, value)

        await self.session.commit()
        await self.session.refresh(weather_to_update)
        return weather_to_update

    async def delete(self, weather: Weather) -> None:
        await self.session.delete(weather)
        await self.session.commit()
