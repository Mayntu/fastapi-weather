from uuid import UUID

from fastapi import APIRouter, Depends

from src.services import get_weather_service
from src.services import WeatherService
from src.schemas import WeatherRead
from src.exceptions import WeatherNotFoundException

router : APIRouter = APIRouter(prefix="/weather")

@router.get("/", response_model=list[WeatherRead])
async def list_weather(
    weather_service: WeatherService = Depends(get_weather_service),
):
    return await weather_service.get_latest_all()


@router.get("/{weather_id}", response_model=WeatherRead)
async def get_weather_by_id(
    weather_id: UUID,
    weather_service: WeatherService = Depends(get_weather_service),
):
    return await weather_service.get_by_id(weather_id)


@router.get("/city/{city}", response_model=WeatherRead)
async def get_weather_by_city(
    city : str,
    weather_service: WeatherService = Depends(get_weather_service)
):
    return await weather_service.get_latest_by_city(city)


@router.post("/refresh", response_model=WeatherRead)
async def refresh_weather(
    city: str,
    country: str | None = None,
    service: WeatherService = Depends(get_weather_service),
):
    return await service.refresh_city(city, country)


@router.delete("/{weather_id}", status_code=204)
async def delete_weather(
    weather_id: UUID,
    weather_service: WeatherService = Depends(get_weather_service)
):
    await weather_service.delete(weather_id)