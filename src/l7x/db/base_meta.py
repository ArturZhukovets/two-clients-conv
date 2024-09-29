#####################################################################################################

from types import MappingProxyType
from typing import Final, TypeVar

from databases import Database
from databases.core import Transaction
from ormar import Extra, Model, OrmarConfig, QuerySet
from sqlalchemy.sql.schema import ColumnCollectionConstraint, MetaData

#####################################################################################################

# from sqlalchemy.util.langhelpers import md5_hex

# _MAX_LEN = 60

# def all_column_names(constraint, table) -> str:
#    ret_str = table.name
#    ret_str += '_'.join((column.name for column in constraint.columns.values()))
#    if len(ret_str) > _MAX_LEN:
#        part1 = ret_str[: _MAX_LEN - 8]
#        part2 = md5_hex(ret_str)[-4:]
#        ret_str = f'{part1}_{part2}'
#    return ret_str

#####################################################################################################

# Default naming convention for all indexes and constraints
# See why this is important and how it would save your time:
# https://docs.sqlalchemy.org/en/20/core/constraints.html#constraint-naming-conventions
# https://alembic.sqlalchemy.org/en/latest/naming.html
_CONVENTION: Final = MappingProxyType({
    'ix': 'ix__%(table_name)s__%(column_0_N_name)s',  # noqa: WPS323

    'uq': 'uq__%(table_name)s__%(column_0_N_name)s',  # noqa: WPS323

    'ck': 'ck__%(table_name)s__%(constraint_name)s',  # noqa: WPS323

    'fk': 'fk__%(table_name)s__%(column_0_N_name)s__%(referred_table_name)s__%(referred_column_0_N_name)s',  # noqa: WPS323

    'pk': 'pk__%(table_name)s',  # noqa: WPS323
})

#####################################################################################################

def create_none_database() -> Database:
    return Database('postgresql+asyncpg://0.0.0.0')

#####################################################################################################

DB_METADATA: Final = MetaData(naming_convention=_CONVENTION)

#####################################################################################################

_BASE_ORMAR_CONFIG: Final = OrmarConfig(
    metadata=DB_METADATA,
    database=create_none_database(),
)

#####################################################################################################

_Model = TypeVar('_Model', bound=Model)

#####################################################################################################

_ORMAR_CONFIGS: Final[list[OrmarConfig]] = []  # noqa: WPS407  # TODO: придумать другое решение

#####################################################################################################

def create_ormar_config(
    *,
    tablename: str | None = None,
    order_by: list[str] | None = None,
    abstract: bool | None = None,
    exclude_parent_fields: list[str] | None = None,
    queryset_class: type[QuerySet[_Model]] | None = None,
    extra: Extra | None = None,
    constraints: list[ColumnCollectionConstraint] | None = None,
) -> OrmarConfig:
    ret: Final = _BASE_ORMAR_CONFIG.copy(
        tablename=tablename,
        order_by=order_by,
        abstract=abstract,
        exclude_parent_fields=exclude_parent_fields,
        queryset_class=queryset_class,
        extra=extra,
        constraints=constraints,
    )
    _ORMAR_CONFIGS.append(ret)
    return ret

#####################################################################################################

def ormar_change_database(database: Database) -> None:
    _BASE_ORMAR_CONFIG.database = database
    for config in _ORMAR_CONFIGS:
        config.database = database

#####################################################################################################

def create_transaction() -> Transaction:
    return _BASE_ORMAR_CONFIG.database.transaction()

#####################################################################################################
