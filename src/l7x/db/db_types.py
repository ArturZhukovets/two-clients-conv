#####################################################################################################

from collections.abc import Callable
from datetime import datetime
from typing import Any, Final, cast
from uuid import UUID as _PYTHON_UUID

from ormar import Boolean, DateTime, String
from ormar.fields.model_fields import ModelFieldFactory
from sqlalchemy.dialects.postgresql import TIMESTAMP as POSTGRESQL_DATETIME, UUID as POSTGRESQL_UUID
from sqlalchemy.dialects.postgresql.pypostgresql import PGDialect_pypostgresql as _Dialect
from sqlalchemy.sql.elements import TextClause
from sqlalchemy.types import TypeDecorator, TypeEngine

from l7x.utils.datetime_utils import UTC_ZONE

#####################################################################################################

_NULLABLE_FIELD_NAME = 'nullable'
_DEFAULT_FIELD_NAME = 'default'
_PRIMARY_KEY_FIELD_NAME = 'primary_key'

#####################################################################################################

class DbString(String):
    #####################################################################################################

    def __new__(cls, *, max_length: int, **kwargs: Any) -> str:  # type: ignore
        return cast(str, super().__new__(cls, max_length=max_length, **kwargs))

    #####################################################################################################

    def __init__(
        self,
        max_length: int,
        min_length: int | None = None,
        regex: str | None = None,
        nullable: bool | None = None,
        default: str | Callable[[], str] | None = None,
    ) -> None:
        kwargs: Final = {
            'max_length': max_length,
            'min_length': min_length,
            'regex': regex,
            _NULLABLE_FIELD_NAME: nullable,
            'default': default,
        }
        super().__init__(**kwargs)

#####################################################################################################

class _DataTimeType(TypeDecorator):  # pylint: disable=abstract-method
    #####################################################################################################

    impl = POSTGRESQL_DATETIME(timezone=True)
    cache_ok = True
    # _LOCAL_TIMEZONE: Final = datetime.utcnow().astimezone().tzinfo

    #####################################################################################################

    def __repr__(self) -> str:
        return 'POSTGRESQL_DATETIME(timezone=True)'

    #####################################################################################################

    @property
    def python_type(self) -> type[datetime]:  # type: ignore
        return datetime

    #####################################################################################################

    def load_dialect_impl(self, dialect: _Dialect) -> TypeEngine:
        obj_type: Final = POSTGRESQL_DATETIME(timezone=True)
        ret: Final = dialect.type_descriptor(obj_type)  # type: ignore
        if not isinstance(ret, TypeEngine):
            type_ret: Final = type(ret)
            raise TypeError(f'dialect.type_descriptor return {type_ret}')
        return ret

    #####################################################################################################

    def process_bind_param(self, value: datetime | None, _dialect: _Dialect) -> datetime | None:  # type: ignore # noqa: WPS110
        if value is None or value.tzinfo is UTC_ZONE:
            return value

        if value.tzinfo is None:
            raise ValueError('Naive datetime is disallowed, see datetime.astimezone')
            # value = value.astimezone(self._LOCAL_TIMEZONE)

        return value.astimezone(UTC_ZONE)

    #####################################################################################################

    def process_result_value(self, value: datetime | None, _dialect: _Dialect) -> datetime | None:  # type: ignore # noqa: WPS110
        if value is None or value.tzinfo is UTC_ZONE:
            return value

        if value.tzinfo is None:
            return value.replace(tzinfo=UTC_ZONE)

        return value.astimezone(UTC_ZONE)

#####################################################################################################

class DbDateTime(DateTime):
    #####################################################################################################

    _type = datetime
    _sample = 'datetime'

    #####################################################################################################

    def __new__(cls, **kwargs: Any) -> datetime:  # type: ignore
        return cast(datetime, super().__new__(cls, timezone=True, **kwargs))

    #####################################################################################################

    def __init__(
        self,
        nullable: bool | None = None,
        default: datetime | Callable[[], datetime] | None = None,
    ) -> None:
        kwargs: Final = {
            _NULLABLE_FIELD_NAME: nullable,
            _DEFAULT_FIELD_NAME: default,
            'timezone': True,
        }
        super().__init__(**kwargs)

    #####################################################################################################

    @classmethod
    def get_column_type(cls, **kwargs: Any) -> Any:
        return _DataTimeType()

#####################################################################################################

class DbBoolean(Boolean):  # type: ignore
    #####################################################################################################

    _type = bool
    _sample = False

    #####################################################################################################

    def __new__(cls, *arg: Any, **kwargs: Any) -> bool:  # type: ignore
        return cast(bool, super().__new__(cls, *arg, **kwargs))

    #####################################################################################################

    def __init__(
        self,
        primary_key: bool | None = False,
        nullable: bool | None = None,
        default: bool | Callable[[], bool] | None = None,
    ) -> None:
        kwargs: Final = {
            _PRIMARY_KEY_FIELD_NAME: primary_key,
            _NULLABLE_FIELD_NAME: nullable,
            _DEFAULT_FIELD_NAME: default,
        }
        super().__init__(**kwargs)

#####################################################################################################

class _UUIDType(TypeDecorator):
    #####################################################################################################

    impl = POSTGRESQL_UUID
    cache_ok = True

    #####################################################################################################

    def __repr__(self) -> str:
        return 'POSTGRESQL_UUID'

    #####################################################################################################

    @property
    def python_type(self) -> type[_PYTHON_UUID]:  # type: ignore
        return _PYTHON_UUID

    #####################################################################################################

    def load_dialect_impl(self, dialect: _Dialect) -> TypeEngine:
        obj_type: Final = POSTGRESQL_UUID()
        ret: Final = dialect.type_descriptor(obj_type)  # type: ignore
        if not isinstance(ret, TypeEngine):
            type_ret: Final = type(ret)
            raise TypeError(f'dialect.type_descriptor return {type_ret}')
        return ret

    #####################################################################################################

    def process_literal_param(  # type: ignore
        self,
        value: _PYTHON_UUID | None,  # noqa: WPS110
        _dialect: _Dialect,
    ) -> _PYTHON_UUID | None:
        return value

    #####################################################################################################

    def process_bind_param(  # type: ignore
        self,
        value: _PYTHON_UUID | None,  # noqa: WPS110
        _dialect: _Dialect,
    ) -> _PYTHON_UUID | None:
        return value

    #####################################################################################################

    def process_result_value(  # type: ignore
        self,
        value: _PYTHON_UUID | None,  # noqa: WPS110
        _dialect: _Dialect,
    ) -> _PYTHON_UUID | None:
        return value

#####################################################################################################

_FIELDS: Final = frozenset(('cls', '__class__', 'kwargs', ))

#####################################################################################################

class DbUUID(ModelFieldFactory, _PYTHON_UUID):
    #####################################################################################################

    _type = _PYTHON_UUID
    _sample = _PYTHON_UUID(int=0)

    #####################################################################################################

    def __new__(cls, *arg: Any, **kwargs: Any) -> _PYTHON_UUID:  # type: ignore
        kwargs_new: Final = {
            **kwargs,
            **{
                item_key: item_val
                for item_key, item_val in locals().items()  # noqa: WPS421
                if item_key not in _FIELDS
            },
        }
        return cast(_PYTHON_UUID, super().__new__(cls, *arg, **kwargs_new))

    #####################################################################################################

    def __init__(
        self,
        primary_key: bool | None = False,
        nullable: bool | None = None,
        default: _PYTHON_UUID | Callable[[], _PYTHON_UUID] | None = None,
        server_default: TextClause | None = None,
    ) -> None:
        kwargs: Final = {
            _PRIMARY_KEY_FIELD_NAME: primary_key,
            _NULLABLE_FIELD_NAME: nullable,
            _DEFAULT_FIELD_NAME: default,
            'server_default': server_default,
        }
        super().__init__(**kwargs)  # type: ignore # pylint: disable=unexpected-keyword-arg

    #####################################################################################################

    @classmethod
    def get_column_type(cls, **kwargs: Any) -> Any:
        return _UUIDType()

#####################################################################################################
