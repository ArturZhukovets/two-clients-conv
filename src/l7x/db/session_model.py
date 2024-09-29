#####################################################################################################

from datetime import datetime
from uuid import UUID

from ormar import ForeignKey, Model
from sqlalchemy import text

from l7x.db.base_meta import create_ormar_config
from l7x.db.db_types import DbDateTime, DbUUID
from l7x.db.user_model import UserModel
from l7x.utils.datetime_utils import now_utc

#####################################################################################################

class SessionModel(Model):
    #####################################################################################################

    primary_uuid: UUID = DbUUID(primary_key=True, server_default=text('gen_random_uuid()'))
    login_ts: datetime = DbDateTime(default=now_utc, nullable=False)
    logout_ts: datetime = DbDateTime(nullable=True)
    user_id: UserModel = ForeignKey(UserModel, nullable=False, related_name='sessions')

    #####################################################################################################

    ormar_config = create_ormar_config(  # type: ignore[pydantic-field]
        tablename='sessions',
    )

#####################################################################################################
