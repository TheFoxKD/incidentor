from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import create_engine, pool

from alembic import context

# Import models so that Alembic autogenerate can discover them.
from src.core.config import Settings
from src.models import incidents  # noqa: F401
from src.models.base import TimestampedBase

config = context.config

if config.config_file_name is not None and Path(config.config_file_name).is_file():
    fileConfig(config.config_file_name)

settings = Settings()
target_metadata = TimestampedBase.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (no engine, only SQL output)."""

    context.configure(
        url=settings.database_sync_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode against a live database."""

    connectable = create_engine(
        settings.database_sync_url,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
