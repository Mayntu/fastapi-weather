from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Weather
from src.schemas import WeatherCreate, WeatherUpdate


class WeatherRepository:
    def __init__(self, session: AsyncSession):
        """Инициализирует репозиторий с сессией базы данных."""
        self.session = session

    async def create(self, data: WeatherCreate) -> Weather:
        """Создает новую запись о погоде."""
        weather : Weather = Weather(**data.model_dump())
        self.session.add(weather)
        await self.session.commit()
        await self.session.refresh(weather)
        return weather

    async def get(self, weather_id) -> Weather | None:
        """Возвращает запись о погоде по ID."""
        return await self.session.get(Weather, weather_id)

    async def many(self, city: str | None = None) -> list[Weather]:
        """Возвращает список всех записей о погоде, опционально фильтруя по городу."""
        stmt = select(Weather)
        if city:
            stmt = stmt.where(Weather.city == city)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update(
        self, weather_to_update: Weather, weather_new_data: WeatherUpdate
    ) -> Weather:
        """Обновляет существующую запись о погоде."""
        for field, value in weather_new_data.model_dump(exclude_unset=True).items():
            setattr(weather_to_update, field, value)

        await self.session.commit()
        await self.session.refresh(weather_to_update)
        return weather_to_update

    async def delete(self, weather: Weather) -> None:
        """Удаляет запись о погоде."""
        await self.session.delete(weather)
        await self.session.commit()

    
    async def get_latest_by_city(self, city: str) -> Weather | None:
        """Возвращает одну последнюю запись для города"""
        stmt = (
            select(Weather)
            .where(Weather.city.ilike(city))
            .order_by(desc(Weather.fetched_at))
            .limit(1)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_latest_for_all_cities(self) -> list[Weather]:
        """
        Возвращает список самых свежих записей для каждого города.
        """
        stmt = (
            select(Weather)
            .distinct(Weather.city)
            .order_by(Weather.city, desc(Weather.fetched_at))
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

