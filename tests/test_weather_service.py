import pytest
from uuid import uuid4
from datetime import datetime, timezone

from src.services import WeatherService, WeatherNotFoundException, WeatherFetcher
from src.models import Weather
from src.repositories import WeatherRepository

@pytest.mark.asyncio
async def test_get_by_id_not_found(
    weather_service : WeatherService,
    mock_repo : WeatherRepository
):
    mock_repo.get.return_value = None
    with pytest.raises(WeatherNotFoundException):
        await weather_service.get_by_id(uuid4())

@pytest.mark.asyncio
async def test_refresh_city_logic(
        weather_service : WeatherService,
        mock_repo : WeatherRepository,
        mock_fetcher : WeatherFetcher
):
    now = datetime.now(timezone.utc)

    weather_data = {
        "city": "London",
        "country": "UK",
        "source": "WeatherAPI",
        "temperature": 20.0,
        "humidity": 50,
        "pressure": 1000,
        "fetched_at": now
    }
    mock_fetcher.fetch.return_value = weather_data
    
    mock_repo.many.return_value = []

    created_weather = Weather(
        id=uuid4(),
        created_at=now,
        updated_at=now,
        **weather_data
    )
    mock_repo.create.return_value = created_weather

    result = await weather_service.refresh_city("London", "UK")

    assert result.city == "London"
    assert mock_repo.create.called


@pytest.mark.asyncio
async def test_get_by_id_success(
    weather_service : WeatherService,
    mock_repo : WeatherRepository
):
    now = datetime.now(timezone.utc)
    weather_obj = Weather(
        id=uuid4(), city="Astana", country="KZ", temperature=10.0,
        humidity=40, pressure=1010, source="test", 
        fetched_at=now, created_at=now, updated_at=now
    )
    mock_repo.get.return_value = weather_obj
    
    result = await weather_service.get_by_id(weather_obj.id)
    
    assert result.id == weather_obj.id
    assert result.city == "Astana"

@pytest.mark.asyncio
async def test_get_latest_all_mapping(
    weather_service : WeatherService,
    mock_repo : WeatherRepository
):
    now = datetime.now(timezone.utc)
    mock_repo.get_latest_for_all_cities.return_value = [
        Weather(id=uuid4(), city="City1", country="C1", temperature=1.0, 
                humidity=1, pressure=1, source="s1", fetched_at=now, 
                created_at=now, updated_at=now),
        Weather(id=uuid4(), city="City2", country="C2", temperature=2.0, 
                humidity=2, pressure=2, source="s2", fetched_at=now, 
                created_at=now, updated_at=now),
    ]
    
    result = await weather_service.get_latest_all()
    
    assert len(result) == 2
    assert result[0].city == "City1"
    assert result[1].city == "City2"

@pytest.mark.asyncio
async def test_delete_success(
    weather_service : WeatherService,
    mock_repo : WeatherRepository
):
    weather_obj = Weather(id=uuid4(), city="To Delete")
    mock_repo.get.return_value = weather_obj
    
    await weather_service.delete(weather_obj.id)
    
    mock_repo.delete.assert_called_once_with(weather_obj)

@pytest.mark.asyncio
async def test_refresh_city_updates_existing(
    weather_service : WeatherService,
    mock_repo : WeatherRepository,
    mock_fetcher : WeatherFetcher
):
    now = datetime.now(timezone.utc)
    weather_data = {
        "city": "London", "country": "UK", "source": "API",
        "temperature": 15.0, "humidity": 80, "pressure": 1000, "fetched_at": now
    }
    mock_fetcher.fetch.return_value = weather_data

    existing_weather = Weather(id=uuid4(), city="London", country="UK")
    mock_repo.many.return_value = [existing_weather]
    
    await weather_service.refresh_city("London", "UK")
    
    assert mock_repo.many.called
    assert mock_repo.update.called
    assert not mock_repo.create.called