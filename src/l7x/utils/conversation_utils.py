#####################################################################################################
from collections.abc import Sequence
from datetime import datetime
from logging import getLogger
from typing import Final

from databases import Database
from nicegui import ui
from nicegui.elements.date import Date
from nicegui.elements.select import Select
from nicegui.elements.table import Table
from nicegui.events import GenericEventArguments
from ormar.fields.sqlalchemy_uuid import UUID

from l7x.db import ConversationModel, DepartmentModel, UserModel
from l7x.logger import DEFAULT_LOGGER_NAME
from l7x.types.localization import TKey
from l7x.utils.datetime_utils import format_datetime_to_iso, q_date_to_utc_datetime, timedelta_to_str, validate_q_date
from l7x.utils.orjson_utils import orjson_dumps_to_str
from l7x.utils.lang_utils import localize as _

#####################################################################################################

async def get_all_conversations(
    start_date: datetime,
    end_date: datetime,
    users: Sequence[UUID] | None = None,
    departments: Sequence[UUID] | None = None,
):
    filters = {
        'start_ts__gte': start_date,
        'start_ts__lte': end_date,
    }
    if users:
        filters['session_id__user_id__primary_uuid__in'] = users
    if departments:
        filters['session_id__user_id__department_id__primary_uuid__in'] = departments

    conversations: Final[Sequence[ConversationModel]] = await ConversationModel.objects.select_related(
        'first_user_session__user_id__department_id',
    ).select_related(
        'second_user_session__user_id__department_id',
    ).filter(
        **filters
    ).order_by(
        ['first_user_session__user_id__department_id', 'first_user_session__user_id', 'start_ts'],
    ).all()

    rows = []
    for conversation in conversations:
        scores = conversation.questionare if conversation.questionare is not None else {}
        row = {
            'primary_uuid': str(conversation.primary_uuid),
            # 'session_id': str(conversation.session_id.primary_uuid),
            'user_name': str(conversation.first_user_session.user_id.full_name),
            'user_login': str(conversation.first_user_session.user_id.login),
            'department_name': str(conversation.first_user_session.user_id.department_id.name),
            'language': conversation.selected_lang,
            'nps_score': scores.get('recommends', '-'),
            'translation_score': scores.get('translation_quality', '-'),
            'usability_score': scores.get('difficulty_of_use', '-'),
            'start_ts': format_datetime_to_iso(conversation.start_ts),
            'end_ts': format_datetime_to_iso(conversation.end_ts) if conversation.end_ts is not None else '',
            'conv_duration': timedelta_to_str(conversation.end_ts - conversation.start_ts) if conversation.end_ts is not None else '',
        }
        rows.append(row)
    return rows

#####################################################################################################

async def get_all_users_for_select() -> dict[UUID, str]:
    users: Sequence[UserModel] = await UserModel.objects.order_by('full_name').all()
    return {user.primary_uuid: user.full_name for user in users}

#####################################################################################################

async def get_all_departments_for_select() -> dict[UUID, str]:
    departments: Sequence[DepartmentModel] = await DepartmentModel.objects.order_by('name').all()
    return {department.primary_uuid: department.name for department in departments}

#####################################################################################################

async def date_validator(start_date_str: str, end_date_str: str):
    if not validate_q_date(start_date_str) or not validate_q_date(end_date_str):
        ui.notify(_(TKey.A_WRONG_DATE_FORMAT), type='negative', position='top')
        return False
    if q_date_to_utc_datetime(start_date_str).date() > q_date_to_utc_datetime(end_date_str).date():
        ui.notify(_(TKey.A_DATE_VALIDATION), type='negative', position='top')
        return False
    return True

#####################################################################################################

async def update_filtered_conversations(
    start_date_str: str,
    end_date_str: str,
    conv_table: Table,
    users: Sequence[UUID] | None = None,
    departments: Sequence[UUID] | None = None,
):
    if not await date_validator(start_date_str, end_date_str):
        return

    start_date = q_date_to_utc_datetime(start_date_str).replace(hour=0, minute=0, second=0)
    end_date = q_date_to_utc_datetime(end_date_str).replace(hour=23, minute=59, second=59)
    curr_date = datetime.now()

    if start_date.date() > curr_date.date():
        conv_table.update_rows([])
        return

    filtered_conversations_rows = await get_all_conversations(start_date, end_date, users, departments)
    conv_table.update_rows(filtered_conversations_rows)

#####################################################################################################

async def clear_filter_conversations(
    start_date: str,
    end_date: str,
    conv_table: Table,
    start_date_calendar: Date,
    end_date_calendar: Date,
    departments_input: Select,
    users_input: Select,
):
    start_date_calendar.set_value(start_date)
    end_date_calendar.set_value(end_date)
    users_input.set_value(None)
    departments_input.set_value(None)
    await update_filtered_conversations(start_date_str=start_date, end_date_str=end_date, conv_table=conv_table)

#####################################################################################################

async def download_all_conversations(conversation_table: Table, start_calendar, end_calendar):
    start_date: Final = start_calendar.value
    end_date: Final = end_calendar.value

    if not await date_validator(start_date, end_date):
        return

    conversation_uuids = [conv['primary_uuid'] for conv in conversation_table.rows]

    async def _download():
        try:
            payload = {
                'primary_uuid': conversation_uuids,
                'is_download_audio': is_download_audio.value,
                'report_format': report_format.value,
            }
            conversation_uuids_str = orjson_dumps_to_str(payload)
            await ui.run_javascript(f'''
                return await (async () => {{
                    try {{
                        const data = await downloadConvData({conversation_uuids_str});
                        return {{ data }};
                    }} catch (error) {{
                        throw new Error(error);
                    }}
                }})();
            ''', timeout=30)
        finally:
            download_popup.close()

    with ui.dialog().classes('w-full') as download_popup:
        with ui.column().classes('download-conv-popup-container'):
            report_format = ui.select(label=_(TKey.A_DOWNLOAD_FORMAT), options=['csv', 'xlsx'], value='xlsx').classes('w-5/6')
            is_download_audio = ui.checkbox(text=_(TKey.A_DOWNLOAD_AUDIO))
            with ui.row():
                ui.button(text=_(TKey.A_DOWNLOAD), on_click=_download)
                ui.button(text=_(TKey.A_CLOSE), on_click=download_popup.close)
    download_popup.open()

#####################################################################################################

async def del_conversation(event: GenericEventArguments, table: Table) -> None:
    data = event.args
    conversation = await ConversationModel.objects.get_or_none(primary_uuid=data['primary_uuid'])

    async def _on_click_delete(conv, tab, popup) -> None:
        try:
            await conv.delete()
            updated_rows = [row for row in tab.rows if row['primary_uuid'] != str(conv.primary_uuid)]
            tab.update_rows(updated_rows)
        except Exception as ex:
            getLogger(DEFAULT_LOGGER_NAME).error(f"Error when delete conversation.", exc_info=ex)
            ui.notify(_(TKey.A_ERROR_DELETE_CONV), type="negative", position="top")
        finally:
            popup.close()

    with ui.dialog().classes('w-full') as conv_delete_popup:
        with ui.column().classes('dep-edit-popup-container'):
            ui.label(_(TKey.A_CONFIRM_DELETE_CONV)).classes('dep-popup-title')
            with ui.row():
                ui.button(_(TKey.A_YES), on_click=lambda _: _on_click_delete(
                    conv=conversation,
                    tab=table,
                    popup=conv_delete_popup,
                )),
                ui.button(_(TKey.A_NO), on_click=conv_delete_popup.close)

    conv_delete_popup.open()

#####################################################################################################

async def check_waiting_conversation(session_id: str, user_id: str):
    try:
        # TODO OPTIMIZE and check why the same user can connect
        conversation = await ConversationModel.objects.filter(
            second_user_session__isnull=True,
            end_ts__isnull=True,
        ).exclude(
            first_user_session__primary_uuid=session_id,
            first_user_session__user_id=user_id,
        ).order_by('-start_ts').limit(1, limit_raw_sql=True).all()
        if not conversation:
            return
        conversation = conversation[0]
    except Exception as ex:
        d = True
        print(ex)
        return
    return conversation

