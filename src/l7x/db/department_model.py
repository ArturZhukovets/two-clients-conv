#####################################################################################################

from typing import cast
from uuid import UUID

from ormar import Model, UniqueColumns
from sqlalchemy import text
from sqlalchemy.schema import ColumnCollectionConstraint

from l7x.db.base_meta import create_ormar_config
from l7x.db.db_types import DbString, DbUUID

#####################################################################################################

class DepartmentModel(Model):
    #####################################################################################################

    primary_uuid: UUID = DbUUID(primary_key=True, server_default=text('gen_random_uuid()'))
    name: str = DbString(max_length=1000, nullable=False)
    address: str = DbString(max_length=1000, nullable=False)
    timezone: str = DbString(max_length=200)  # example +03:00

    #####################################################################################################

    ormar_config = create_ormar_config(  # type: ignore[pydantic-field]
        tablename='departments',
    )

#####################################################################################################
