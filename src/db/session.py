from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine
from src.core.config import settings

engine : AsyncEngine = create_async_engine(
    url=settings.DB_URL,
    echo=settings.DEBUG,
)

AsyncSessionLocal : async_sessionmaker = async_sessionmaker(
    engine,
    expire_on_commit=False,
)
