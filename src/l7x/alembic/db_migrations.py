#####################################################################################################

from asyncio import run as _asyncio_run
from typing import Final

from alembic.context import (
    begin_transaction as _alembic_begin_transaction,
    config as _alembic_config,
    configure as _alembic_configure,
    is_offline_mode as _alembic_is_offline_mode,
    run_migrations as _alembic_run_migrations,
)
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine

from l7x.db.base_meta import DB_METADATA
from l7x.types.errors import AppException

#####################################################################################################

def _run_migrations_offline() -> None:
    url: Final = _alembic_config.get_main_option('sqlalchemy.url')
    _alembic_configure(
        url=url,
        target_metadata=DB_METADATA,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with _alembic_begin_transaction():
        _alembic_run_migrations()

#####################################################################################################

def _do_run_migrations(connection: Connection) -> None:
    _alembic_configure(connection=connection, target_metadata=DB_METADATA)

    with _alembic_begin_transaction():
        _alembic_run_migrations()

#####################################################################################################

async def _run_migrations_online() -> None:
    config_section: Final = _alembic_config.get_section(_alembic_config.config_ini_section)
    if config_section is None:
        raise AppException('Invalid alembic config section.')

    connectable: Final = AsyncEngine(
        engine_from_config(
            config_section,
            prefix='sqlalchemy.',
            poolclass=pool.NullPool,
            future=True,
        ),
    )

    async with connectable.connect() as connection:  # type: ignore
        await connection.run_sync(_do_run_migrations)

    await connectable.dispose()  # type: ignore

#####################################################################################################

def run_db_migrations() -> None:
    if _alembic_is_offline_mode():
        _run_migrations_offline()
    else:
        _asyncio_run(_run_migrations_online())

#####################################################################################################
