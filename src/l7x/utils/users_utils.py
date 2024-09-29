from logging import getLogger
from typing import Final

from argon2 import PasswordHasher
from nicegui import ui
from nicegui.element import Element
from nicegui.elements.button import Button
from nicegui.elements.dialog import Dialog
from nicegui.elements.table import Table
from nicegui.events import GenericEventArguments
from nicegui.functions.notify import notify

from l7x.db import UserModel, SessionModel
from l7x.logger import DEFAULT_LOGGER_NAME
from l7x.types.localization import TKey
from l7x.utils.departments_utils import create_departments_options
from l7x.utils.ui_elements import popup_spinner, required_text, spinner_handler
from l7x.utils.lang_utils import localize as _

#####################################################################################################

async def _update_or_add_user(
    user_data: dict[str, str],
    table: Table,
    popup: Dialog,
    password_hasher: PasswordHasher,
    spinner: Element | None = None,
    buttons_for_disable: list[Button] | None = None
) -> None:
    data = user_data
    is_new_user = data.get('primary_uuid') is None
    new_password = data['password'].strip()

    if is_new_user:
        if not new_password:
            ui.notify(_(TKey.A_PASSWORD_EMPTY), position='top', type='negative')
            return
        elif not data['login']:
            ui.notify(_(TKey.A_LOGIN_EMPTY), position='top', type='negative')
            return
        elif not data['full_name']:
            ui.notify(_(TKey.A_FULL_NAME_EMPTY), position='top', type='negative')
            return
        elif not data['department_id']:
            ui.notify(_(TKey.A_SELECT_DEPARTMENT), position='top', type='negative')
            return
    await spinner_handler(spinner, buttons_for_disable, start=True)
    try:
        if is_new_user:
            password = password_hasher.hash(data.pop('password'))
            user = await UserModel(**data, password=password).upsert()
        else:
            user = await UserModel.objects.get(primary_uuid=data['primary_uuid'])
            if not new_password:
                data.pop('password')
                await user.upsert(**data)
            else:
                password = password_hasher.hash(data.pop('password'))
                await user.upsert(**data, password=password)

        new_rows = []
        for row in table.rows:
            if row['primary_uuid'] == str(user.primary_uuid):
                new_rows.append({
                    'primary_uuid': str(user.primary_uuid),
                    'login': user.login,
                    'full_name': user.full_name,
                    'ip_v4': user.ip_v4,
                    'is_active': user.is_active,
                    'is_superuser': user.is_superuser,
                    'department_id': str(user.department_id.primary_uuid),
                })
            else:
                new_rows.append(row)

        if user_data.get('primary_uuid') is None:
            new_rows.append({
                'primary_uuid': str(user.primary_uuid),
                'login': user.login,
                'full_name': user.full_name,
                'ip_v4': user.ip_v4,
                'is_active': user.is_active,
                'is_superuser': user.is_superuser,
                'department_id': str(user.department_id.primary_uuid),
            })
        table.update_rows(new_rows)
        popup.close()
    except BaseException:
        if is_new_user:
            ui.notify(
                message=_(TKey.A_ERROR_CREATE_USER),
                type='negative',
                position='top',
            )
        else:
            ui.notify(
                message=_(TKey.A_ERROR_EDIT_USER),
            )
    finally:
        await spinner_handler(spinner, buttons_for_disable, start=False)

#####################################################################################################

async def get_all_users() -> list[dict]:
    users = await UserModel.objects.all()
    rows = []
    for user in users:
        rows.append({
            'primary_uuid': str(user.primary_uuid),
            'login': user.login,
            'full_name': user.full_name,
            'ip_v4': user.ip_v4,
            'is_active': user.is_active,
            'is_superuser': user.is_superuser,
            'create_at': user.create_at,
            'department_id': str(user.department_id.primary_uuid),
        })
    return rows

#####################################################################################################

async def _update_and_del_user(user: UserModel, tab: Table, popup: Dialog) -> None:
    try:
        await SessionModel.objects.filter(user_id=user.primary_uuid).delete()
        await user.delete()
        updated_rows = [row for row in tab.rows if row['primary_uuid'] != str(user.primary_uuid)]
        tab.update_rows(updated_rows)
    except Exception as ex:
        getLogger(DEFAULT_LOGGER_NAME).error(f"Error when delete user.", exc_info=ex)
        ui.notify(_(TKey.A_BASE_ERROR_DELETE_USER), type="negative", position="top")
    finally:
        popup.close()

#####################################################################################################

async def del_user(event: GenericEventArguments, table: Table) -> None:
    data = event.args
    u_id = data['primary_uuid']
    s_id = event.client.request.cookies['session_uuid']
    session = await SessionModel.objects.get_or_none(primary_uuid=s_id)
    if str(session.user_id.primary_uuid) == u_id:
        notify(
            message=_(TKey.A_USER_DEL_HIMSELF),
            position='top',
            type='negative',
        )
        return
    user = await UserModel.objects.prefetch_related('sessions__conversations').get(primary_uuid=data['primary_uuid'])
    count_conv = 0
    for session in user.sessions:
        count_conv += len(session.conversations)

    if count_conv > 0:
        notify(
            f'{_(TKey.A_ERROR_DELETE_USER)}. {_(TKey.A_DIALOGS_COUNT)} {count_conv}',
            position='top',
            type='negative',
        )
    else:
        with ui.dialog().classes('w-full') as user_delete_popup:
            with ui.column().classes('dep-edit-popup-container'):
                ui.label(f'{_(TKey.A_CONFIRM_DELETE_USER)} "{user.full_name}" ?').classes('dep-popup-title')
                with ui.row():
                    ui.button(_(TKey.A_YES), on_click=lambda _: _update_and_del_user(
                        user,
                        tab=table,
                        popup=user_delete_popup,
                    )),
                    ui.button(_(TKey.A_NO), on_click=user_delete_popup.close)

        user_delete_popup.open()

#####################################################################################################

async def edit_user(
    event: GenericEventArguments,
    table: Table,
    password_hasher: PasswordHasher,
    active_user: UserModel
) -> None:
    data = event.args
    user = await UserModel.objects.get_or_none(primary_uuid=data['primary_uuid'])
    departments_opts = await create_departments_options()
    is_self_user = str(active_user.primary_uuid) == data.get('primary_uuid')

    if user is None:
        ui.notify(_(TKey.A_ERROR_EDIT_USER), position='top', type='negative')
    else:
        with ui.dialog().classes('w-full') as user_edit_popup:
            with ui.column().classes('dep-edit-popup-container'):
                u_login_in = ui.input(label=_(TKey.LOGIN), value=user.login).props('outlined').classes('required')
                u_pass_in = ui.input(label=_(TKey.A_NEW_USER_PASSWORD)).props('outlined')
                u_full_name_in = ui.input(label=_(TKey.A_FULL_NAME), value=user.full_name).props('outlined').classes('required')
                u_ip_v4_in = ui.input(label='IPv4 Address', value=user.ip_v4).props('outlined')
                u_department_select = ui.select(
                    label=_(TKey.A_DEPARTMENT),
                    options=departments_opts,
                    value=str(user.department_id.primary_uuid)
                ).classes('dep-select required-select')
                await required_text()
                if not is_self_user:
                    u_is_active_cbx = ui.checkbox(text=_(TKey.A_IS_ACTIVE), value=user.is_active)
                    u_is_superuser_cbx = ui.checkbox(text=_(TKey.A_ADMINISTRATOR), value=user.is_superuser)

                with ui.row():
                    edit_btn = ui.button(_(TKey.A_EDIT), on_click=lambda _: _update_or_add_user(
                        {
                            'primary_uuid': str(user.primary_uuid),
                            'login': u_login_in.value,
                            'password': u_pass_in.value,
                            'full_name': u_full_name_in.value,
                            'department_id': u_department_select.value,
                            'is_active': data['is_active'] if is_self_user else u_is_active_cbx.value,
                            'ip_v4': u_ip_v4_in.value,
                            'is_superuser': data['is_active'] if is_self_user else u_is_superuser_cbx.value,
                        },
                        table=table,
                        popup=user_edit_popup,
                        password_hasher=password_hasher,
                        spinner=spinner,
                        buttons_for_disable=[edit_btn, close_btn]
                    ))
                    close_btn = ui.button(_(TKey.A_CANCEL), on_click=user_edit_popup.close)
                spinner = await popup_spinner()

        user_edit_popup.open()

#####################################################################################################

async def create_user(table: Table, password_hasher: PasswordHasher) -> None:
    departments_opts: Final = await create_departments_options()

    with ui.dialog().classes('w-full') as user_create_popup:
        with ui.column().classes('dep-edit-popup-container'):
            u_login_in = ui.input(label=_(TKey.LOGIN)).props('outlined').classes('required')
            u_pass_in = ui.input(label=_(TKey.PASSWORD)).props('outlined').classes('required')
            u_full_name_in = ui.input(label=_(TKey.A_FULL_NAME)).props('outlined').classes('required')
            u_ip_v4_in = ui.input(label='IPv4 Address').props('outlined')
            u_department_select = ui.select(label=_(TKey.A_DEPARTMENT), options=departments_opts, value=None).classes('dep-select required-select')
            await required_text()
            u_is_active_cbx = ui.checkbox(text=_(TKey.A_IS_ACTIVE), value=True)
            u_is_superuser_cbx = ui.checkbox(text=_(TKey.A_ADMINISTRATOR), value=False)

            with ui.row():
                create_btn = ui.button(_(TKey.A_CREATE), on_click=lambda _: _update_or_add_user(
                    {
                        'login': u_login_in.value,
                        'password': u_pass_in.value,
                        'full_name': u_full_name_in.value,
                        'department_id': u_department_select.value,
                        'is_active': u_is_active_cbx.value,
                        'ip_v4': u_ip_v4_in.value,
                        'is_superuser': u_is_superuser_cbx.value
                    },
                    table=table,
                    popup=user_create_popup,
                    password_hasher=password_hasher,
                    spinner=spinner,
                    buttons_for_disable=[create_btn, close_btn],
                ))
                close_btn = ui.button(_(TKey.A_CANCEL), on_click=user_create_popup.close)
            spinner = await popup_spinner()

    user_create_popup.open()

#####################################################################################################
