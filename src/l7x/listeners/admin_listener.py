#####################################################################################################
from datetime import datetime, timedelta, timezone
from logging import Logger
from typing import Final

from nicegui import ui
from starlette.requests import Request

from l7x.db import SessionModel
from l7x.types.language import LKey
from l7x.types.localization import TKey
from l7x.utils.conversation_utils import (
    clear_filter_conversations,
    download_all_conversations,
    get_all_conversations,
    get_all_departments_for_select,
    get_all_users_for_select,
    update_filtered_conversations,
    del_conversation,
)
from l7x.utils.datetime_utils import datetime_to_q_date, datetime_to_q_date_props
from l7x.utils.departments_utils import create_department, del_department, edit_department, get_all_departments
from l7x.utils.fastapi_utils import AppFastAPI
from l7x.utils.lang_utils import create_lang_list

from l7x.utils.nicegui_utils import TableColumn
from l7x.utils.transcribe_analytics_utils import (
    clear_filter_audio_analysis,
    download_all_audio_cases,
    get_edited_texts,
    update_filtered_audio_analysis,
)
from l7x.utils.ui_elements import calendar_element
from l7x.utils.users_utils import create_user, del_user, edit_user, get_all_users

#####################################################################################################

ROWS_PER_PAGE: Final = 10

#####################################################################################################

SORT_TZ_FUNC: Final = '''
    (a, b, rowA, rowB) => {
        function getTimezoneOffsetInMinutes (timezone) {
            const sign = timezone[0];
            const hours = parseInt(timezone.substring(1, 3), 10);
            const minutes = parseInt(timezone.substring(4), 10);
            let offset = hours * 60 + minutes;
            if (sign === '-') {
                offset *= -1;
            }
            return offset;
        };

        return getTimezoneOffsetInMinutes(a) - getTimezoneOffsetInMinutes(b);
        }
'''

#####################################################################################################

# TODO ИСПОЛЬЗОВАТЬ ФУНКЦИЮ localize Для всех вызовов локализации

def _dep_cols(logger: Logger, lang: LKey) -> list[TableColumn]:
    return [
        {'name': 'primary_uuid', 'label': 'UUID', 'field': 'primary_uuid', 'align': 'center'},
        {'name': 'name', 'label': TKey.A_NAME(logger, lang), 'field': 'name', 'align': 'center', 'sortable': True},
        {'name': 'address', 'label': TKey.A_ADDRESS(logger, lang), 'field': 'address', 'align': 'center', 'sortable': True},
        {
            'name': 'timezone', 'label': TKey.A_TIME_ZONE(logger, lang), 'field': 'timezone', 'align': 'center',
            'sortable': True, ':sort': SORT_TZ_FUNC
        },
    ]

#####################################################################################################

def _users_cols(logger: Logger, lang: LKey) -> list[TableColumn]:
    return [
        {'name': 'primary_uuid', 'label': 'UUID', 'field': 'primary_uuid', 'align': 'center'},
        {'name': 'login', 'label': TKey.A_USER_LOGIN(logger, lang), 'field': 'login', 'align': 'center', 'sortable': True},
        {'name': 'full_name', 'label': TKey.A_FULL_NAME(logger, lang), 'field': 'full_name', 'align': 'center', 'sortable': True},
        {'name': 'ip_v4', 'label': 'IP', 'field': 'ip_v4', 'align': 'center'},
        {'name': 'is_active', 'label': TKey.A_IS_ACTIVE(logger, lang), 'field': 'is_active', 'align': 'center', 'sortable': True},
        {'name': 'is_superuser', 'label': TKey.A_ADMINISTRATOR(logger, lang), 'field': 'is_superuser', 'align': 'center',
         'sortable': True},
        {'name': 'department_id', 'label': TKey.A_DEPARTMENT_UUID(logger, lang), 'field': 'department_id', 'align': 'center',
         'sortable': True},
    ]

#####################################################################################################

def _conv_cols(logger: Logger, lang: LKey, enable_admin_pages: bool) -> list[TableColumn]:
    if not enable_admin_pages:
        return [
            {'name': 'department_name', 'label': TKey.A_DEPARTMENT(logger, lang), 'field': 'department_name', 'align': 'center',
             'sortable': True},
            {'name': 'user_name', 'label': TKey.A_USER(logger, lang), 'field': 'user_name', 'align': 'center', 'sortable': True},
            {'name': 'user_login', 'label': TKey.A_USER_LOGIN(logger, lang), 'field': 'user_login', 'align': 'center',
             'sortable': True},
            # {'name': 'session_id', 'label': TKey.A_SESSION_UUID(logger, lang), 'field': 'session_id', 'align': 'center', 'sortable': True},
            {'name': 'primary_uuid', 'label': TKey.A_DIALOG_UUID(logger, lang), 'field': 'primary_uuid', 'align': 'center', 'sortable': True},
            {'name': 'language', 'label': TKey.A_LANGUAGE(logger, lang), 'field': 'language', 'align': 'center', 'sortable': True},
            {'name': 'start_ts', 'label': TKey.A_DIALOG_START(logger, lang), 'field': 'start_ts', 'align': 'center', 'sortable': True},
            {'name': 'end_ts', 'label': TKey.A_DIALOG_END(logger, lang), 'field': 'end_ts', 'align': 'center', 'sortable': True},
            {'name': 'conv_duration', 'label': TKey.A_DIALOG_DURATION(logger, lang), 'field': 'conv_duration', 'align': 'center',
             'sortable': True},
        ]
    return [
        {'name': 'department_name', 'label': TKey.A_DEPARTMENT(logger, lang), 'field': 'department_name', 'align': 'center',
         'sortable': True},
        {'name': 'user_name', 'label': TKey.A_USER(logger, lang), 'field': 'user_name', 'align': 'center', 'sortable': True},
        {'name': 'user_login', 'label': TKey.A_USER_LOGIN(logger, lang), 'field': 'user_login', 'align': 'center',
         'sortable': True},
        {'name': 'session_id', 'label': TKey.A_SESSION_UUID(logger, lang), 'field': 'session_id', 'align': 'center', 'sortable': True},
        {'name': 'primary_uuid', 'label': TKey.A_DIALOG_UUID(logger, lang), 'field': 'primary_uuid', 'align': 'center', 'sortable': True},
        {'name': 'language', 'label': TKey.A_LANGUAGE(logger, lang), 'field': 'language', 'align': 'center', 'sortable': True},
        {'name': 'nps_score', 'label': TKey.A_NPS_SCORE(logger, lang), 'field': 'nps_score', 'align': 'center', 'sortable': True},
        {'name': 'translation_score', 'label': TKey.A_TRANSLATION_SCORE(logger, lang), 'field': 'translation_score', 'align': 'center',
         'sortable': True},
        {'name': 'usability_score', 'label': TKey.A_USABILITY_SCORE(logger, lang), 'field': 'usability_score', 'align': 'center',
         'sortable': True},
        {'name': 'start_ts', 'label': TKey.A_DIALOG_START(logger, lang), 'field': 'start_ts', 'align': 'center', 'sortable': True},
        {'name': 'end_ts', 'label': TKey.A_DIALOG_END(logger, lang), 'field': 'end_ts', 'align': 'center', 'sortable': True},
        {'name': 'conv_duration', 'label': TKey.A_DIALOG_DURATION(logger, lang), 'field': 'conv_duration', 'align': 'center',
         'sortable': True},
    ]


#####################################################################################################

def _transcribe_analytic_cols(logger: Logger, lang: LKey) -> list[TableColumn]:
    return [
        {'name': 'primary_uuid', 'label': TKey.A_MESSAGE_UUID(logger, lang), 'field': 'primary_uuid', 'align': 'center', 'sortable': True},
        {'name': 'create_date', 'label': TKey.A_CREATION_DATE(logger, lang), 'field': 'create_date', 'align': 'center', 'sortable': True},
        {'name': 'transcribe_text', 'label': TKey.A_RECOGNIZED_TEXT(logger, lang), 'field': 'transcribe_text', 'align': 'center', 'sortable': True},
        {'name': 'edited_text', 'label': TKey.A_EDITED_TEXT(logger, lang), 'field': 'edited_text', 'align': 'center', 'sortable': True},
        {'name': 'language', 'label': TKey.A_LANGUAGE(logger, lang), 'field': 'language', 'align': 'center', 'sortable': True},
        {'name': 'audio_url', 'label': TKey.A_AUDIO(logger, lang), 'field': 'audio_url', 'align': 'center', 'sortable': True},
    ]

#####################################################################################################

async def _admin_page(request: Request) -> None:
    app: Final = request.app
    default_lang: Final = LKey(app.app_settings.default_language_locale)
    current_sess = await SessionModel.objects.get(primary_uuid=request.cookies['session_uuid'])
    current_user = current_sess.user_id
    current_date = datetime.now()
    start_date = current_date - timedelta(days=7)
    start_date_replaced = start_date.replace(hour=0, minute=0, second=0, tzinfo=timezone.utc)
    end_date_replaced = current_date.replace(hour=23, minute=59, second=59, tzinfo=timezone.utc)
    last_date_props = f''':options="date => date <= '{datetime_to_q_date_props(current_date)}'"'''
    ui.add_head_html('<link rel="stylesheet" href="./static/style.css">')
    ui.add_body_html('<script src="./static/admin_script.js"></script>')
    with ui.splitter(limits=(12, 12), value=12).classes('w-full h-full rounded-xl') as splitter:

        with splitter.before:
            with ui.tabs().props('vertical').classes('w-full h-full') as tabs:
                departments_tab = ui.tab(
                    TKey.A_DEPARTMENTS(app.logger, default_lang),
                    icon='home_work'
                ).style('white-space: normal')
                users_tab = ui.tab(
                    name=TKey.A_USERS(app.logger, default_lang),
                    icon='manage_accounts'
                ).style('white-space: normal')
                conversations_tab = ui.tab(
                    name=TKey.A_DIALOGS(app.logger, default_lang),
                    icon='speaker_notes'
                ).style('white-space: normal')
                transcribe_analysis_tab = ui.tab(
                    name=TKey.A_RECOGNITION_ERRORS(app.logger, default_lang),
                    icon='lyrics'
                ).style('white-space: normal')

        with splitter.after:
            with ui.tab_panels(tabs, value=departments_tab).props('vertical').classes('w-full h-full rounded-r-xl'):

                # =================================================== DEPARTMENTS PANEL

                with ui.tab_panel(departments_tab).classes('w-full h-full'):
                    with ui.scroll_area().classes('w-full h-full border'):
                        with ui.table(
                            columns=_dep_cols(app.logger, default_lang),
                            rows=await get_all_departments(),
                            pagination=ROWS_PER_PAGE,
                        ).classes('w-full') as dep_table:
                            dep_table.add_slot(
                                'header',
                                fr'''
                                    <q-tr :props="props">
                                        <q-th v-for="col in props.cols" :key="col.name" :props="props">
                                            {{{{ col.label }}}}
                                        </q-th>
                                        <q-th>{TKey.A_EDIT(app.logger, default_lang)}</q-th>
                                        <q-th>{TKey.A_DELETE(app.logger, default_lang)}</q-th>
                                    </q-tr>
                            ''')

                            dep_table.add_slot(
                                'body',
                                r'''
                                    <q-tr :props="props">
                                        <q-td v-for="col in props.cols" :key="col.name" :props="props">
                                            {{ col.value }}
                                        </q-td>
                                        <q-td auto-width class="text-center">
                                            <q-btn size="sm" color="green" round dense
                                                @click="$parent.$emit('edit', props.row)"
                                                icon="edit" />
                                        </q-td>
                                        <q-td auto-width class="text-center">
                                            <q-btn size="sm" color="red" round dense
                                                @click="$parent.$emit('delete', props.row)"
                                                icon="delete" />
                                        </q-td>
                                    </q-tr>
                            ''')
                            dep_table.on('delete', lambda e: del_department(e, dep_table))
                            dep_table.on('edit', lambda e: edit_department(e, dep_table))
                    ui.button(text=TKey.A_CREATE(app.logger, default_lang), on_click=lambda e: create_department(dep_table))

                # =================================================== USER PANEL

                with ui.tab_panel(users_tab).classes('w-full h-full'):
                    with ui.scroll_area().classes('w-full h-full border'):
                        with ui.table(
                            columns=_users_cols(app.logger, default_lang),
                            rows=await get_all_users(),
                            pagination=ROWS_PER_PAGE,
                        ).classes('w-full') as users_table:
                            users_table.add_slot(
                                'header',
                                fr'''
                                    <q-tr :props="props">
                                        <q-th v-for="col in props.cols" :key="col.name" :props="props">
                                            {{{{ col.label }}}}
                                        </q-th>
                                        <q-th>{TKey.A_EDIT(app.logger, default_lang)}</q-th>
                                        <q-th>{TKey.A_DELETE(app.logger, default_lang)}</q-th>
                                </q-tr>
                            ''')

                            users_table.add_slot(
                                'body',
                                r'''
                                    <q-tr :props="props">
                                        <q-td v-for="col in props.cols" :key="col.name" :props="props">
                                            {{ col.value }}
                                        </q-td>
                                        <q-td auto-width class="text-center">
                                            <q-btn size="sm" color="green" round dense
                                                @click="$parent.$emit('edit', props.row)"
                                                icon="edit" />
                                        </q-td>
                                        <q-td auto-width class="text-center">
                                            <q-btn size="sm" color="red" round dense
                                                @click="$parent.$emit('delete', props.row)"
                                                icon="delete" />
                                        </q-td>
                                    </q-tr>
                            ''')
                            users_table.on('delete', lambda e: del_user(e, users_table))
                            users_table.on('edit', lambda e: edit_user(e, users_table, app.password_hasher, current_user))
                    ui.button(text=TKey.A_CREATE(app.logger, default_lang), on_click=lambda e: create_user(users_table, app.password_hasher))

                ######################### CONVERSATIONS PANEL ###############################

                with ui.tab_panel(conversations_tab).classes('w-full h-full'):
                    with ui.row().classes('admin-calendar-container'):
                        start_date_in, start_calendar = await calendar_element(
                            placeholder=TKey.A_FROM(app.logger, default_lang),
                            value=datetime_to_q_date(start_date),
                            props=last_date_props,
                        )
                        end_date_in, end_calendar = await calendar_element(
                            placeholder=TKey.A_TO(app.logger, default_lang),
                            value=datetime_to_q_date(current_date),
                            props=last_date_props,
                        )
                        user_selector = ui.select(
                            options=await get_all_users_for_select(),
                            label=TKey.A_USERS(app.logger, default_lang),
                            multiple=True,
                            clearable=True,
                            with_input=True,
                        ).props(
                            'outlined'
                        ).classes('admin-calendar-container-input')
                        department_selector = ui.select(
                            options=await get_all_departments_for_select(),
                            label=TKey.A_DEPARTMENTS(app.logger, default_lang),
                            multiple=True,
                            clearable=True,
                            with_input=True,
                        ).props(
                            'outlined'
                        ).classes('admin-calendar-container-input')
                        with ui.row().classes('admin-calendar-container-btn-block'):
                            ui.button(
                                text=TKey.A_FILTER(app.logger, default_lang),
                                on_click=lambda _: update_filtered_conversations(
                                    start_date_str=start_calendar.value,
                                    end_date_str=end_calendar.value,
                                    departments=department_selector.value,
                                    users=user_selector.value,
                                    conv_table=conversation_table,
                                ),
                            )
                            ui.button(
                                text=TKey.A_RESET(app.logger, default_lang),
                                on_click=lambda _: clear_filter_conversations(
                                    start_date=datetime_to_q_date(start_date_replaced),
                                    end_date=datetime_to_q_date(end_date_replaced),
                                    conv_table=conversation_table,
                                    start_date_calendar=start_calendar,
                                    end_date_calendar=end_calendar,
                                    departments_input=department_selector,
                                    users_input=user_selector,
                                )
                            )
                    with ui.scroll_area().classes('w-full h-full border'):
                        with ui.table(
                            columns=_conv_cols(app.logger, default_lang, app.app_settings.enable_questionnaire),
                            rows=await get_all_conversations(
                                start_date=start_date.replace(hour=0, minute=0, second=0, tzinfo=timezone.utc),
                                end_date=current_date.replace(hour=23, minute=59, second=59, tzinfo=timezone.utc),
                            ),
                            pagination=ROWS_PER_PAGE,
                        ).classes('w-full') as conversation_table:
                            conversation_table.add_slot(
                                'header',
                                fr'''
                                    <q-tr :props="props">
                                        <q-th v-for="col in props.cols" :key="col.name" :props="props">
                                            {{{{ col.label }}}}
                                        </q-th>
                                        <q-th>{TKey.A_DOWNLOAD(app.logger, default_lang)}</q-th>
                                        <q-th>{TKey.A_DELETE(app.logger, default_lang)}</q-th>
                                </q-tr>
                            ''')

                            conversation_table.add_slot(
                                'body',
                                r'''
                                    <q-tr :props="props">
                                        <q-td v-for="col in props.cols" :key="col.name" :props="props">
                                            {{ col.value }}
                                        </q-td>
                                        <q-td auto-width class="text-center">
                                            <q-btn size="sm" color="green" round dense
                                                @click="$parent.$emit('download', props.row)"
                                                icon="download" />
                                        </q-td>
                                        <q-td auto-width class="text-center">
                                            <q-btn size="sm" color="red" round dense
                                                @click="$parent.$emit('delete', props.row)"
                                                icon="delete" />
                                        </q-td>
                                    </q-tr>
                            ''')
                            conversation_table.on('download', js_handler='downloadConvData')
                            conversation_table.on('delete', lambda e: del_conversation(e, conversation_table))
                    ui.button(
                        text=TKey.A_DOWNLOAD_ALL(app.logger, default_lang),
                        on_click=lambda _: download_all_conversations(conversation_table, start_calendar, end_calendar),
                    )

                # =================================================== TRANSCRIBE ANALYSIS

                with ui.tab_panel(transcribe_analysis_tab).classes('w-full h-full'):
                    with ui.row().classes('admin-calendar-container'):
                        aa_start_date_in, aa_start_calendar = await calendar_element(
                            placeholder=TKey.A_FROM(app.logger, default_lang),
                            value=datetime_to_q_date(start_date),
                            props=last_date_props,
                        )
                        aa_end_date_in, aa_end_calendar = await calendar_element(
                            placeholder=TKey.A_TO(app.logger, default_lang),
                            value=datetime_to_q_date(current_date),
                            props=last_date_props,
                        )
                        aa_lang_selector = ui.select(
                            options=await create_lang_list(app),
                            label=TKey.A_LANGUAGE(app.logger, default_lang),
                            multiple=True,
                            clearable=True,
                            with_input=True,
                        ).props(
                            'outlined'
                        ).classes('admin-calendar-container-input')

                        with ui.row().classes('admin-calendar-container-btn-block'):
                            ui.button(
                                text=TKey.A_FILTER(app.logger, default_lang),
                                on_click=lambda _: update_filtered_audio_analysis(
                                    start_date_str=aa_start_calendar.value,
                                    end_date_str=aa_end_calendar.value,
                                    languages=aa_lang_selector.value,
                                    audio_analysis_table=audio_analysis_table,
                                ),
                            )
                            ui.button(
                                text=TKey.A_RESET(app.logger, default_lang),
                                on_click=lambda _: clear_filter_audio_analysis(
                                    start_date=datetime_to_q_date(start_date_replaced),
                                    end_date=datetime_to_q_date(end_date_replaced),
                                    audio_analysis_table=audio_analysis_table,
                                    start_date_calendar=aa_start_calendar,
                                    end_date_calendar=aa_end_calendar,
                                    language_input=aa_lang_selector,
                                )
                            )
                    with ui.scroll_area().classes('w-full h-full border'):
                        with ui.table(
                            columns=_transcribe_analytic_cols(app.logger, default_lang),
                            rows=await get_edited_texts(
                                start_date=start_date.replace(hour=0, minute=0, second=0, tzinfo=timezone.utc),
                                end_date=current_date.replace(hour=23, minute=59, second=59, tzinfo=timezone.utc),
                            ),
                            pagination=ROWS_PER_PAGE,
                        ).classes('w-full wrap-table') as audio_analysis_table:
                            audio_analysis_table.add_slot(
                                'header',
                                r'''
                                    <q-tr :props="props">
                                        <q-th v-for="col in props.cols" :key="col.name" :props="props">
                                            {{ col.label }}
                                        </q-th>
                                </q-tr>
                            ''')

                            audio_analysis_table.add_slot(
                                'body',
                                r'''
                                    <q-tr :props="props">
                                        <q-td v-for="col in props.cols" :key="col.name" :props="props">
                                                <template v-if="col.name !== 'audio_url'">
                                                    {{ col.value }}
                                                </template>
                                                <template v-else>
                                                    <audio
                                                        :src="col.value"
                                                        style="width:240px;height:45px" controls
                                                        controlslist="nofullscreen noplaybackrate"
                                                        preload="none"
                                                    ></audio>
                                                </template>
                                        </q-td>
                                    </q-tr>
                            ''')
                            audio_analysis_table.on('download', js_handler='downloadConvData')
                    ui.button(
                        text=TKey.A_DOWNLOAD_ALL(app.logger, default_lang),
                        on_click=lambda _: download_all_audio_cases(audio_analysis_table, start_calendar, end_calendar),
                    )


#####################################################################################################

def admin_page_listener_registrar(app: AppFastAPI, /) -> None:
    if app.app_settings.enable_admin_pages:
        ui.page('/admin', response_timeout=30)(_admin_page)

#####################################################################################################
