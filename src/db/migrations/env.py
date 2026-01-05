import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# 1. ИМПОРТИРУЕМ НАСТРОЙКИ И БАЗОВУЮ МОДЕЛЬ
from src.core.config import settings
from src.db import Base
from src.models import Weather 

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 2. УКАЗЫВАЕМ METADATA
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    # 3. ПОДСТАВЛЯЕМ URL ИЗ SETTINGS
    url = settings.DB_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    # 4. ДИНАМИЧЕСКИ СОЗДАЕМ CONFIG
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.DB_URL

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()