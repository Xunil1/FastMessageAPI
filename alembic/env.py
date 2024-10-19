import asyncio

from sqlalchemy.ext.asyncio import AsyncEngine
from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import create_engine
from db.base import Base  # импортируйте ваши модели
from core.config import settings  # ваша конфигурация БД

# Пример для асинхронного SQLAlchemy
def run_migrations_online():
    connectable = AsyncEngine(
        create_engine(
            settings.DATABASE_URL,
            poolclass=pool.NullPool,
            future=True
        )
    )

    async def run_migrations():
        async with connectable.connect() as connection:
            await connection.run_sync(Base.metadata.create_all)
            await connection.run_sync(do_run_migrations)

    async def do_run_migrations(connection):
        context.configure(connection=connection, target_metadata=Base.metadata)

        with context.begin_transaction():
            context.run_migrations()

    asyncio.run(run_migrations())