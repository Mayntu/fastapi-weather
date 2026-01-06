from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.core.config import settings
from src.db.session import AsyncSessionLocal
from src.repositories import WeatherRepository
from src.services import WeatherFetcher, WeatherService, get_http_client

from loguru import logger as log


scheduler = AsyncIOScheduler()


async def refresh_all_cities():
    async with AsyncSessionLocal() as session:
        repo = WeatherRepository(session)
        fetcher = WeatherFetcher(await get_http_client())
        service = WeatherService(repo, fetcher)

        for item in settings.DEFAULT_CITIES:
            city, country = item.split(",")
            try:
                await service.refresh_city(city, country)
            except Exception as e:
                log.error(f"Failed to refresh {city}: {e}")


def start_scheduler():
    scheduler.add_job(
        refresh_all_cities,
        trigger="interval",
        minutes=10,
        id="refresh_weather",
        replace_existing=True,
        # next_run_time=datetime.now()
    )
    scheduler.start()
