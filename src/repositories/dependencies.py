from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_session
from src.repositories import WeatherRepository

def get_weather_repo(session: AsyncSession = Depends(get_session)) -> WeatherRepository:
    return WeatherRepository(session)