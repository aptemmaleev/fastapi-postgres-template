import asyncio
import os
import sys
from logging.config import fileConfig
from alembic import context
from dotenv import load_dotenv

from sqlalchemy import pool, Column
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlmodel import SQLModel

load_dotenv()

sys.path.append(".")

from app.models import *

config = context.config
fileConfig(config.config_file_name)
target_metadata = SQLModel.metadata

config.set_main_option("sqlalchemy.url", os.getenv("POSTGRES_URL"))


def run_migrations_offline() -> None:
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        render_as_batch=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async def run():
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)

    asyncio.run(run())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
