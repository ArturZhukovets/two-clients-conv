from collections.abc import Sequence
from datetime import datetime
from typing import Final

from nicegui import ui
from nicegui.elements.date import Date
from nicegui.elements.select import Select
from nicegui.elements.table import Table

from l7x.db import TextModel
from l7x.types.localization import TKey
from l7x.utils.conversation_utils import date_validator
from l7x.utils.datetime_utils import format_datetime_to_iso, q_date_to_utc_datetime
from l7x.utils.orjson_utils import orjson_dumps_to_str
from l7x.utils.lang_utils import localize as _


async def get_edited_texts(
    start_date: datetime,
    end_date: datetime,
    languages: Sequence[str] | None = None,
):
    filters = {
        'create_ts__gte': start_date,
        'create_ts__lte': end_date,
        'audio_id__isnull': False,
        'edit_ts__isnull': False,
    }
    if languages:
        filters['lang_from__in'] = languages

    texts: Final[Sequence[TextModel]] = await TextModel.objects.filter(
        **filters
    ).order_by(
        ['create_ts'],
    ).all()

    rows = []

    for text in texts:
        rec_text = text.recognized_text.strip(),
        fixed_text = text.fixed_text.strip()
        if rec_text == fixed_text:
            continue

        row = {
            'primary_uuid': str(text.primary_uuid),
            'create_date': format_datetime_to_iso(text.create_ts),
            'transcribe_text': text.recognized_text,
            'edited_text': text.fixed_text,
            'language': text.lang_from,
            'audio_url': f'/api/audio_file/{text.audio_id.primary_uuid}'
        }
        rows.append(row)

    return rows

#####################################################################################################

async def update_filtered_audio_analysis(
    start_date_str: str,
    end_date_str: str,
    audio_analysis_table: Table,
    languages: Sequence[str] | None = None,
):
    if not await date_validator(start_date_str, end_date_str):
        return

    start_date = q_date_to_utc_datetime(start_date_str).replace(hour=0, minute=0, second=0)
    end_date = q_date_to_utc_datetime(end_date_str).replace(hour=23, minute=59, second=59)
    curr_date = datetime.now()

    if start_date.date() > curr_date.date():
        audio_analysis_table.update_rows([])
        return

    filtered_conversations_rows = await get_edited_texts(start_date, end_date, languages)
    audio_analysis_table.update_rows(filtered_conversations_rows)

#####################################################################################################

async def clear_filter_audio_analysis(
    start_date: str,
    end_date: str,
    audio_analysis_table: Table,
    start_date_calendar: Date,
    end_date_calendar: Date,
    language_input: Select,
):
    start_date_calendar.set_value(start_date)
    end_date_calendar.set_value(end_date)
    language_input.set_value(None)
    await update_filtered_audio_analysis(
        start_date_str=start_date,
        end_date_str=end_date,
        audio_analysis_table=audio_analysis_table,
    )

#####################################################################################################

async def download_all_audio_cases(audio_analysis_table: Table, start_calendar, end_calendar):
    start_date: Final = start_calendar.value
    end_date: Final = end_calendar.value

    if not await date_validator(start_date, end_date):
        return

    text_uuids = [text['primary_uuid'] for text in audio_analysis_table.rows]

    async def _download_analysis():
        try:
            payload = {
                'primary_uuid': text_uuids,
                'report_format': report_format.value,
            }
            text_uuids_str = orjson_dumps_to_str(payload)

            await ui.run_javascript(f'''
                return await (async () => {{
                    try {{
                        const data = await downloadTextData({text_uuids_str});
                        return {{ data }};
                    }} catch (error) {{
                        throw new Error(error);
                    }}
                }})();
            ''', timeout=30)
        finally:
            download_analysis_popup.close()

    with ui.dialog().classes('w-full') as download_analysis_popup:
        with ui.column().classes('download-conv-popup-container'):
            report_format = ui.select(label=_(TKey.A_DOWNLOAD_FORMAT), options=['csv', 'xlsx'], value='xlsx').classes('w-5/6')
            with ui.row():
                ui.button(text=_(TKey.A_DOWNLOAD), on_click=_download_analysis)
                ui.button(text=_(TKey.A_CLOSE), on_click=download_analysis_popup.close)
    download_analysis_popup.open()

#####################################################################################################
