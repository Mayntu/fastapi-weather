import pytest
from src.main import app
from src.services import get_weather_service, WeatherNotFoundException, WeatherService

from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock
from uuid import uuid4

@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_get_all_weather_endpoint(client : AsyncClient):
    mock_service : WeatherService = AsyncMock()
    mock_service.get_latest_all.return_value = []

    app.dependency_overrides[get_weather_service] = lambda: mock_service
    
    response = await client.get("/api/v1/weather/")
    
    assert response.status_code == 200
    assert response.json() == []

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_city_weather_404(client : AsyncClient):
    mock_service : WeatherService = AsyncMock()

    mock_service.get_latest_by_city.side_effect = WeatherNotFoundException()
    
    app.dependency_overrides[get_weather_service] = lambda: mock_service
    
    response = await client.get("/api/v1/weather/city/NonExistent")
    
    assert response.status_code == 404
    assert "Weather not found for city".lower() in response.json()["detail"].lower()
    
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_delete_weather_endpoint(client : AsyncClient):
    mock_service : WeatherService = AsyncMock()
    mock_service.delete.return_value = None
    
    app.dependency_overrides[get_weather_service] = lambda: mock_service
    
    test_id = uuid4()
    response = await client.delete(f"/api/v1/weather/{test_id}")
    
    assert response.status_code == 204
    app.dependency_overrides.clear()