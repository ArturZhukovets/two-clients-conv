from collections.abc import Sequence
from typing import Final

from starlette.requests import Request

from l7x.db import ConversationModel, SessionModel
from l7x.utils.datetime_utils import now_utc

#####################################################################################################

class SessionNotFound(Exception):
    """NOTHING."""

#####################################################################################################

class SessionClosed(Exception):
    """NOTHING."""

#####################################################################################################

class UserNotActive(Exception):
    """NOTHING."""

#####################################################################################################


async def get_session_with_conversations(session_uuid) -> SessionModel | None:
    return await SessionModel.objects.select_related(
        'user_id',
    ).prefetch_related(
        'first_user_conversations'
    ).prefetch_related(
        'second_user_conversations'
    ).get_or_none(
        primary_uuid=session_uuid,
    )

#####################################################################################################

async def close_conversations(conversations: Sequence[ConversationModel]) -> None:
    for conversation in conversations:
        if conversation.end_ts is None:
            await conversation.update(end_ts=now_utc())

#####################################################################################################

async def close_sessions_and_conversations(user_uuid) -> None:
    user_sessions = await SessionModel.objects.prefetch_related(
        'conversations',
    ).filter(
        user_id__primary_uuid=user_uuid,
        logout_ts__isnull=True,
    ).all()
    for user_session in user_sessions:
        await user_session.update(logout_ts=now_utc())
        await close_conversations(user_session.conversations)

#####################################################################################################

async def check_valid_session(session_uuid: str) -> None:
    session: Final[SessionModel | None] = await get_session_with_conversations(session_uuid)

    if session is None:
        raise SessionNotFound

    if session.logout_ts is not None:
        session_conversations = []
        if session.first_user_conversations:
            session_conversations.extend(session.first_user_conversations)
        if session.second_user_conversations:
            session_conversations.extend(session.second_user_conversations)
        await close_conversations(session_conversations)
        raise SessionClosed

    if not session.user_id.is_active:
        await close_sessions_and_conversations(session.user_id.primary_uuid)
        raise UserNotActive

#####################################################################################################

async def check_session_with_request(request: Request, action_str: str) -> bool:
    session_uuid: Final = request.cookies.get('session_uuid')
    logger: Final = request.app.logger
    if session_uuid is None:
        logger.warning(f'Can`t {action_str}. session_uuid in cookie not found')
        return False
    session = await SessionModel.objects \
        .prefetch_related('first_user_conversations').prefetch_related('second_user_conversations') \
        .get_or_none(primary_uuid=session_uuid)
    if session is None:
        logger.warning(f'Can`t {action_str}. Session is not valid')
        return False
    if session.logout_ts is not None:
        logger.warning(f'Can`t {action_str}. This session has been closed')
        for conversation in session.first_user_conversations:
            if conversation.end_ts is None:
                await conversation.update(end_ts=now_utc())
        for conversation in session.second_user_conversations:
            if conversation.end_ts is None:
                await conversation.update(end_ts=now_utc())
        return False
    return True

#####################################################################################################

async def check_superuser_state(request: Request) -> bool:
    session_uuid: Final = request.cookies.get('session_uuid')
    logger: Final = request.app.logger
    try:
        session: SessionModel = await SessionModel.objects \
            .select_related('user_id') \
            .get_or_none(primary_uuid=session_uuid)
        if session is not None:
            if session.user_id.is_superuser:
                return True
        return False
    except BaseException as err:
        logger.warning(f'Can`t check superuser state for session UUID. Error: {err}')
        return False

#####################################################################################################
