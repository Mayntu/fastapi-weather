import httpx

from datetime import datetime, timezone
from loguru import logger as log

from src.core import settings

class WeatherFetcher:
    def __init__(self, client : httpx.AsyncClient) -> None:
        self.client = client
    
    async def fetch(self, city : str, country : str):
        params : dict = {
            "key" : settings.WEATHER_API_KEY,
            "q": f"{city}",
            "aqi" : "no",
        }
        if country:
            params["q"] += f",{country}"

        response = await self.client.get(
            settings.WEATHER_API_URL,
            params=params
        )
        response.raise_for_status()
        
        data : dict = response.json()
        
        country = data.get("location").get("country") if not country else country

        current : dict = data.get("current")
        if not current:
            raise ValueError("Weather not found")
        
        result : dict = {
            "city" : city,
            "country" : country,
            "temperature": current["temp_c"],
            "humidity": current["humidity"],
            "pressure": int(current["pressure_mb"]),
            "source": "weatherapi.com",
            "fetched_at": datetime.now(tz=timezone.utc),
        }
        return result
