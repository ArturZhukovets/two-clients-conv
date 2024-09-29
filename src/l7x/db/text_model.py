#####################################################################################################

from datetime import datetime
from typing import Literal
from uuid import UUID

from ormar import ForeignKey, Model, Text, ReferentialAction
from pytest_recording.utils import unique
from sqlalchemy import text

from l7x.db import SessionModel
from l7x.db.audio_model import AudioModel
from l7x.db.base_meta import create_ormar_config
from l7x.db.conversation_model import ConversationModel
from l7x.db.db_types import DbDateTime, DbString, DbUUID
from l7x.utils.datetime_utils import now_utc

#####################################################################################################

TextType = Literal['operator', 'client', 'feedback']

#####################################################################################################

class TextModel(Model):
    #####################################################################################################

    primary_uuid: UUID = DbUUID(primary_key=True, server_default=text('gen_random_uuid()'))
    create_ts: datetime = DbDateTime(default=now_utc)
    edit_ts: datetime = DbDateTime(nullable=True)
    audio_id: AudioModel | None = ForeignKey(AudioModel, nullable=True, related_name='audio')  # TODO Сделать One-to-one
    lang_from: str = DbString(max_length=30)
    lang_to: str = DbString(max_length=30)
    recognized_text: str = Text()
    translated_text: str = Text()
    fixed_text: str = Text(nullable=True)
    owner_session_uuid: SessionModel = ForeignKey(
        SessionModel,
        nullable=True,
        ondelete=ReferentialAction.SET_NULL,
    )
    conversation_id: ConversationModel = ForeignKey(
        ConversationModel,
        nullable=False,
        related_name='texts',
        ondelete=ReferentialAction.CASCADE,
    )

    #####################################################################################################

    ormar_config = create_ormar_config(  # type: ignore[pydantic-field]
        tablename='texts',
    )

#####################################################################################################
