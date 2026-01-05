import httpx

from datetime import datetime, timezone

from src.core import settings

class WeatherFetcher:
    def __init__(self, client : httpx.AsyncClient) -> None:
        self.client = client
    
    async def fetch(self, city : str, country : str):
        params : dict = {
            "key" : settings.WEATHER_API_KEY,
            "q": f"{city},{country}",
            "aqi" : "no",
        }

        response = await self.client.get(
            settings.WEATHER_API_URL,
            params=params
        )
        response.raise_for_status()
        
        data : dict = response.json()
        print(data)
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
