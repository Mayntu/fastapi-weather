from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class WeatherBase(BaseModel):
    city: str
    country: str
    temperature: float
    humidity: int
    pressure: int
    source: str
    fetched_at: datetime

    class Config:
        from_attributes = True


class WeatherCreate(WeatherBase):
    country: str | None


class WeatherUpdate(BaseModel):
    temperature: float | None = None
    humidity: int | None = None
    pressure: int | None = None
    fetched_at: datetime | None = None


class WeatherRead(WeatherBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
