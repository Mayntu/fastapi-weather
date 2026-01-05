from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.db import get_session
from src.services import get_weather_service
from src.services import WeatherService, WeatherNotFoundException
from src.repositories import WeatherRepository
from src.schemas import (
    WeatherCreate,
    WeatherRead,
    WeatherUpdate,
)

router : APIRouter = APIRouter(prefix="/weather")

@router.get("/", response_model=list[WeatherRead])
async def list_weather(
    city: str | None = None,
    weather_service: WeatherService = Depends(get_weather_service),
):
    return await weather_service.get_many(city=city)


@router.get("/{weather_id}", response_model=WeatherRead)
async def get_weather_by_id(
    weather_id: UUID,
    weather_service: WeatherService = Depends(get_weather_service),
):
    try:
        return await weather_service.get_by_id(weather_id)
    except WeatherNotFoundException:
        raise HTTPException(status_code=404, detail="Weather not found")


@router.post("/refresh", response_model=WeatherRead)
async def refresh_weather(
    city: str,
    country: str,
    service: WeatherService = Depends(get_weather_service),
):
    try:
        return await service.refresh_city(city, country)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 


# @router.put("/{weather_id}", response_model=WeatherRead)
# async def update_weather(
#     weather_id: UUID,
#     data: WeatherUpdate,
#     session: AsyncSession = Depends(get_session),
# ):
#     repo = WeatherRepository(session)
#     weather = await repo.get(weather_id)
#     if not weather:
#         raise HTTPException(status_code=404, detail="Not found")

#     return await repo.update(weather, data)


@router.delete("/{weather_id}", status_code=204)
async def delete_weather(
    weather_id: UUID,
    weather_service: WeatherService = Depends(get_weather_service)
):
    try:
        await weather_service.delete(weather_id)
    except WeatherNotFoundException:
        raise HTTPException(status_code=404, detail="Weather not found")