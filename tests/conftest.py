import pytest
from unittest.mock import AsyncMock

from src.services import WeatherService

@pytest.fixture
def mock_repo():
    return AsyncMock()

@pytest.fixture
def mock_fetcher():
    return AsyncMock()

@pytest.fixture
def weather_service(mock_repo, mock_fetcher):
    return WeatherService(repo=mock_repo, weather_fetcher=mock_fetcher)