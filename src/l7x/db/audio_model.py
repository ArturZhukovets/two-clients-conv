#####################################################################################################

from datetime import datetime
from uuid import UUID

from ormar import LargeBinary, Model
from sqlalchemy import text

from l7x.db.base_meta import create_ormar_config
from l7x.db.db_types import DbDateTime, DbUUID
from l7x.utils.datetime_utils import now_utc

#####################################################################################################

class AudioModel(Model):
    #####################################################################################################

    primary_uuid: UUID = DbUUID(primary_key=True, server_default=text('gen_random_uuid()'))
    create_ts: datetime = DbDateTime(default=now_utc)
    audio_raw: bytes = LargeBinary(max_length=100*1024*1024, nullable=False)

    #####################################################################################################

    ormar_config = create_ormar_config(  # type: ignore[pydantic-field]
        tablename='audio',
    )

#####################################################################################################
