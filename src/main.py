from fastapi import FastAPI

from src.core import settings
from src.routers.v1 import weather_router

app : FastAPI = FastAPI(title=settings.APP_NAME)

app.include_router(
    router=weather_router,
    prefix=settings.API_V1_PREFIX,
    tags=["Weather"]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="0.0.0.0", port=8000, reload=True)
