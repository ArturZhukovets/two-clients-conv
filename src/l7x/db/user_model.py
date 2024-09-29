#####################################################################################################

from datetime import datetime
from typing import cast
from uuid import UUID

from ormar import Boolean, ForeignKey, Model, UniqueColumns
from sqlalchemy import text
from sqlalchemy.schema import ColumnCollectionConstraint
from sqlalchemy.sql import false as _sql_false

from l7x.db.base_meta import create_ormar_config
from l7x.db.db_types import DbDateTime, DbString, DbUUID
from l7x.db.department_model import DepartmentModel
from l7x.utils.datetime_utils import now_utc

#####################################################################################################

class UserModel(Model):
    #####################################################################################################

    primary_uuid: UUID = DbUUID(primary_key=True, server_default=text('gen_random_uuid()'))
    login: str = DbString(max_length=200)
    full_name: str = DbString(max_length=1000)
    password: str = DbString(max_length=500)
    ip_v4: str = DbString(max_length=15, nullable=True)
    is_active: bool = Boolean(default=True)
    is_superuser: bool = Boolean(default=False, server_default=_sql_false(), nullable=False)
    create_at: datetime = DbDateTime(default=now_utc)
    department_id: DepartmentModel = ForeignKey(DepartmentModel, related_name='users')

    #####################################################################################################

    ormar_config = create_ormar_config(  # type: ignore[pydantic-field]
        tablename='users',
        constraints=[cast(ColumnCollectionConstraint, UniqueColumns('login'))],
    )

#####################################################################################################
