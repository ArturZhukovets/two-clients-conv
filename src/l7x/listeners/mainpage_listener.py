#####################################################################################################
from typing import Final, Callable, Coroutine, Sequence

import ormar
from nicegui import ui
from nicegui.elements.dialog import Dialog
from nicegui.observables import ObservableDict
from starlette.requests import Request

from l7x.configs.settings import AppSettings
from l7x.db import ConversationModel, SessionModel
from l7x.types.language import LKey
from l7x.types.localization import TKey
from l7x.utils.datetime_utils import now_utc
from l7x.utils.fastapi_utils import AppFastAPI
from l7x.utils.nicegui_utils import GuiProcessor, prepare_session_storage
from l7x.utils.pages import (
    dialog_page_gui,
    final_page_gui,
    header_gui,
    recommendation_survay_page_gui,
    review_page_gui,
    select_lang_page_gui,
    translation_quality_survay_page_gui,
    use_translator_survay_page_gui,
)

#####################################################################################################
def _get_available_pages(app_settings: AppSettings) -> Sequence[Callable[[GuiProcessor, ObservableDict], Coroutine]]:
    if not app_settings.enable_questionnaire:
        return (
            select_lang_page_gui,
            dialog_page_gui,
        )
    return (
        select_lang_page_gui,
        dialog_page_gui,
        use_translator_survay_page_gui,
        recommendation_survay_page_gui,
        translation_quality_survay_page_gui,
        review_page_gui,
        final_page_gui,
    )

#####################################################################################################

async def _check_active_session(session: SessionModel):
    if session is not None:
        other_sessions = await SessionModel.objects.filter(
            user_id__primary_uuid=session.user_id,
            logout_ts__isnull=True
        ).exclude(primary_uuid=session.primary_uuid).all()
        return other_sessions

#####################################################################################################

async def close_not_active_sessions(sessions: list[SessionModel], pop_up: Dialog = None) -> None:
    for session in sessions:
        await session.update(logout_ts=now_utc())
    if pop_up is not None:
        pop_up.close()

#####################################################################################################

async def get_last_unclosed_conversation(session: SessionModel) -> ConversationModel:
    """Find last unclosed conversation of specified session"""
    conversations = await ConversationModel.objects.filter(
        ormar.or_(
            first_user_session__primary_uuid=session.primary_uuid,
            second_user_session__primary_uuid=session.primary_uuid,
        )
    ).order_by(
        '-start_ts'
    ).limit(1, limit_raw_sql=True).all()
    if conversations:
        conversation = conversations[0]
        if conversation.end_ts is None:
            return conversation

#####################################################################################################

async def _show_mainpage(request: Request) -> None:
    app: Final = request.app
    _default_lang = app.app_settings.default_language_locale
    session_uuid: Final = request.cookies.get('session_uuid')
    session: Final = await SessionModel.objects.select_related('user_id__department_id').get(primary_uuid=session_uuid)
    user: Final = session.user_id
    session_storage: Final = prepare_session_storage(app.storage.client)

    gui_processor = GuiProcessor(
        session_storage,
        session_uuid,
        user,
        app,
        _get_available_pages(app.app_settings)
    )

    other_active_sessions = await _check_active_session(session)

    if other_active_sessions:
        with ui.dialog() as close_session_dialog:
            with ui.column().classes('close-sessions-popup'):
                ui.label(
                    f'{TKey.THE_USER(app.logger, LKey(_default_lang))} '
                    f'"{user.full_name}" '
                    f'{TKey.HAS_MORE_THAN_ONE_SESSION(app.logger, LKey(_default_lang))}.'
                )
                ui.label(f'{TKey.TOTAL_OPEN_SESSIONS(app.logger, LKey(_default_lang))}: {len(other_active_sessions) + 1}.')
                with ui.row().classes('w-full justify-center'):
                    ui.button(
                        text=TKey.CLOSE_ALL_SESSIONS(app.logger, LKey(_default_lang)),
                        on_click=lambda _: close_not_active_sessions(other_active_sessions, close_session_dialog),
                    )
                    ui.button(
                        text=TKey.LEAVE_ALL_SESSIONS_OPEN(app.logger, LKey(_default_lang)),
                        on_click=close_session_dialog.close,
                    )
            close_session_dialog.open()

    ####################### LOAD CSS and JS #######################

    ui.add_head_html('<link rel="stylesheet" href="./static/main_style.css">')
    ui.add_head_html('<link rel="stylesheet" href="./static/style.css">')
    ui.add_body_html('<script src="./static/main_script.js"></script>')

    await header_gui(gui_processor, session_storage)

    page_container = ui.column().classes('my-page-container')
    gui_processor.page_container = page_container

    last_unclosed_conversation = await get_last_unclosed_conversation(session)

    if last_unclosed_conversation:
        conv_in_storage = app.conversations_storage.get_conv(conv_id=last_unclosed_conversation.primary_uuid)
        if conv_in_storage:
            selected_lang = conv_in_storage.get_selected_lang_by_session(session_id=session_uuid)
            if selected_lang is None:
                await gui_processor.init_start_page(conversation=last_unclosed_conversation)
            else:
                await gui_processor.restore_conversation(conversation=last_unclosed_conversation)
    else:
        await gui_processor.init_start_page()

#####################################################################################################

def mainpage_listener_registrar(app: AppFastAPI, /) -> None:
    ui.page('/', response_timeout=500)(_show_mainpage)

#####################################################################################################

