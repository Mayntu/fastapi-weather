from src.db.session import AsyncSessionLocal


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session