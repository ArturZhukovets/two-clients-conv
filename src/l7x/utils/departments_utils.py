from typing import Final

from nicegui import ui
from nicegui.element import Element
from nicegui.elements.button import Button
from nicegui.elements.dialog import Dialog
from nicegui.elements.table import Table
from nicegui.events import GenericEventArguments

from l7x.db import DepartmentModel
from l7x.types.localization import TKey
from l7x.utils.datetime_utils import validate_time_offset
from l7x.utils.ui_elements import popup_spinner, required_text, spinner_handler
from l7x.utils.lang_utils import localize as _

#####################################################################################################

async def _update_or_add_department(
    dep_data: dict[str, str],
    table: Table,
    popup: Dialog,
    spinner: Element | None = None,
    buttons_for_disable: list[Button] | None = None,
) -> None:
    is_new_dep = dep_data.get('primary_uuid') is None
    if not dep_data.get('name'):
        ui.notify(_(TKey.A_DEP_NAME_EMPTY), type='negative', position='top')
        return
    if not validate_time_offset(dep_data.get('timezone')):
        ui.notify(_(TKey.A_INCORRECT_TIME_ZONE), type='negative', position='top')
        return
    await spinner_handler(spinner, buttons_for_disable, start=True)
    try:
        department = await DepartmentModel(**dep_data).upsert()
        new_rows = []
        for row in table.rows:
            if row['primary_uuid'] == str(department.primary_uuid):
                new_rows.append({
                    'primary_uuid': str(department.primary_uuid),
                    'name': department.name,
                    'address': department.address,
                    'timezone': department.timezone,
                })
            else:
                new_rows.append(row)

        if is_new_dep:
            new_rows.append({
                'primary_uuid': str(department.primary_uuid),
                'name': department.name,
                'address': department.address,
                'timezone': department.timezone,
            })

        table.update_rows(new_rows)
        popup.close()
    except BaseException:
        if is_new_dep:
            ui.notify(
                message=_(TKey.A_ERROR_CREATE_DEP),
                type='negative',
                position='top',
            )
        else:
            ui.notify(
                message=_(TKey.A_ERROR_EDIT_DEP),
                type='negative',
                position='top',
            )
    finally:
        await spinner_handler(spinner, buttons_for_disable, start=False)

#####################################################################################################

async def get_all_departments() -> list[dict[str, str]]:
    departments = await DepartmentModel.objects.all()
    rows = [{'primary_uuid': str(d.primary_uuid), 'name': d.name, 'address': d.address, 'timezone': d.timezone} for d in departments]
    return rows

#####################################################################################################

async def _update_and_del_department(dep: DepartmentModel, tab: Table, popup: Dialog) -> None:
    new_rows = []
    for row in tab.rows:
        if row['primary_uuid'] != str(dep.primary_uuid):
            new_rows.append(row)
    tab.update_rows(new_rows)
    await dep.delete()
    popup.close()

#####################################################################################################

async def del_department(event: GenericEventArguments, table: Table) -> None:
    data = event.args
    department = await DepartmentModel.objects.prefetch_related('users').get_or_none(primary_uuid=data['primary_uuid'])
    related_usernames = [f'{num +1}) {user.full_name}' for num, user in enumerate(department.users)]
    if related_usernames:
        users_str = ', '.join(related_usernames)
        ui.notify(f'{_(TKey.A_UNABLE_TO_DELETE_DEP)}:{users_str}', multi_line=True, position='top', type='negative')
    else:
        with ui.dialog().classes('w-full') as dep_delete_popup:
            with ui.column().classes('dep-edit-popup-container'):
                ui.label(f'{_(TKey.A_APPROVE_DELETION)} "{department.name}" ?').classes('dep-popup-title ')
                with ui.row():
                    ui.button(_(TKey.A_YES), on_click=lambda _: _update_and_del_department(
                        department,
                        tab=table,
                        popup=dep_delete_popup,
                    )),
                    ui.button(_(TKey.A_NO), on_click=dep_delete_popup.close)

        dep_delete_popup.open()

#####################################################################################################

async def edit_department(event: GenericEventArguments, table: Table) -> None:
    data = event.args
    department: Final[DepartmentModel] = await DepartmentModel.objects.get_or_none(primary_uuid=data['primary_uuid'])
    if department is None:
        ui.notify(_(TKey.A_UNABLE_TO_EDIT), position='top', type='negative')
        return
    with ui.dialog().classes('w-full') as dep_edit_popup:
        with ui.column().classes('dep-edit-popup-container'):
            dep_name_in = ui.input(label=_(TKey.A_NAME), value=department.name).props('outlined').classes('required')
            dep_addr_in = ui.input(label=_(TKey.A_ADDRESS), value=department.address).props('outlined')
            dep_tz_in = ui.input(
                label=_(TKey.A_TIME_ZONE), placeholder='+03:00', value=department.timezone,
            ).props('outlined').classes('required')
            await required_text()
            with ui.row():
                edit_btn = ui.button(_(TKey.A_EDIT), on_click=lambda _: _update_or_add_department(
                    {
                        'primary_uuid': data['primary_uuid'],
                        'name': dep_name_in.value,
                        'address': dep_addr_in.value,
                        'timezone': dep_tz_in.value,
                    },
                    table=table,
                    popup=dep_edit_popup,
                    spinner=spinner,
                    buttons_for_disable=[edit_btn, close_btn],
                ))
                close_btn = ui.button(_(TKey.A_CANCEL), on_click=dep_edit_popup.close)
            spinner = await popup_spinner()

    dep_edit_popup.open()

#####################################################################################################

async def create_department(table: Table):
    with ui.dialog().classes('w-full') as dep_edit_popup:
        with ui.column().classes('dep-edit-popup-container'):
            dep_name_in = ui.input(label=_(TKey.A_NAME)).props('outlined ').classes('required')
            dep_addr_in = ui.input(label=_(TKey.A_ADDRESS)).props('outlined')
            dep_tz_in = ui.input(label=_(TKey.A_TIME_ZONE), placeholder='+03:00').props('outlined').classes('required')
            await required_text()
            with ui.row():
                create_btn = ui.button(_(TKey.A_CREATE), on_click=lambda _: _update_or_add_department(
                    {
                        'name': dep_name_in.value,
                        'address': dep_addr_in.value,
                        'timezone': dep_tz_in.value,
                    },
                    table=table,
                    popup=dep_edit_popup,
                    spinner=spinner,
                    buttons_for_disable=[create_btn, close_btn],
                ))
                close_btn = ui.button(_(TKey.A_CANCEL), on_click=dep_edit_popup.close)
            spinner = await popup_spinner()

    dep_edit_popup.open()

#####################################################################################################

async def create_departments_options() -> dict[str, str]:
    departments = await DepartmentModel.objects.order_by('name').all()
    return {str(d.primary_uuid): d.name for d in departments}

#####################################################################################################
