from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from src.core import (
    settings,
    validation_exception_handler,
    setup_logging,
    weather_exception_handler
)
from src.tasks import start_weather_scheduler
from src.services import get_http_client
from src.routers.v1 import weather_router
from src.exceptions import WeatherException

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    client = await get_http_client()
    start_weather_scheduler()

    yield

    await client.aclose()

app : FastAPI = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.include_router(
    router=weather_router,
    prefix=settings.API_V1_PREFIX,
    tags=["Weather"]
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(WeatherException, weather_exception_handler)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="0.0.0.0", port=8000, reload=True)
