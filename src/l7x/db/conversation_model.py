#####################################################################################################

from datetime import datetime
from uuid import UUID

from ormar import JSON, ForeignKey, Model
from pydantic import Json
from sqlalchemy import text

from l7x.db import SessionModel
from l7x.db.base_meta import create_ormar_config
from l7x.db.db_types import DbDateTime, DbString, DbUUID
from l7x.utils.datetime_utils import now_utc

#####################################################################################################

class ConversationModel(Model):
    #####################################################################################################

    primary_uuid: UUID = DbUUID(primary_key=True, server_default=text('gen_random_uuid()'))
    start_ts: datetime = DbDateTime(default=now_utc, nullable=False)
    end_ts: datetime = DbDateTime(nullable=True)
    selected_lang: str = DbString(max_length=30, nullable=True)  # Todo Это ненужное поле
    questionare: Json = JSON(nullable=True)
    first_user_session: SessionModel = ForeignKey(
        SessionModel,
        nullable=False,
        related_name='first_user_conversations'
    )
    second_user_session: SessionModel = ForeignKey(
        SessionModel,
        nullable=True,
        related_name='second_user_conversations',
    )

    #####################################################################################################

    ormar_config = create_ormar_config(  # type: ignore[pydantic-field]
        tablename='conversations',
    )

    @classmethod
    async def close_all_unclosed(cls) -> None:
        """Closes all conversations that are not closed."""
        d = True
        await cls.objects.filter(end_ts__isnull=True).update(end_ts=now_utc())
        print("All unclosed conversations were closed")
#####################################################################################################
