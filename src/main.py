from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager

from src.core import settings, validation_exception_handler, setup_logging
from src.tasks import start_weather_scheduler
from src.routers.v1 import weather_router
from src.services import get_http_client

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="0.0.0.0", port=8000, reload=True)
