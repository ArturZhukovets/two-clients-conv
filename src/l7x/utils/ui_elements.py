from asyncio import sleep

from nicegui import ui
from nicegui.element import Element
from nicegui.elements.date import Date
from nicegui.elements.input import Input

from l7x.types.localization import TKey
from l7x.utils.datetime_utils import validate_q_date
from l7x.utils.lang_utils import localize as _


#####################################################################################################

async def required_text() -> None:
    inner_text = _(TKey.A_REQUIRED_FIELDS)
    ui.html(f'<div class="required-text"><span style="color:red">*</span> - {inner_text} </div>')

#####################################################################################################

async def popup_spinner() -> Element:
    spinner = ui.element('span').classes('popup-spinner')
    spinner.set_visibility(False)
    return spinner

#####################################################################################################

async def spinner_handler(spinner, buttons_for_disable, start=True) -> None:
    if spinner is not None:
        spinner.set_visibility(start)
    if buttons_for_disable is not None:
        for button in buttons_for_disable:
            button.set_enabled(not start)
    await sleep(0.2)

#####################################################################################################

async def calendar_element(placeholder: str, *, value: str, props: str = '') -> tuple[Input, Date]:
    _wrong_format = _(TKey.A_WRONG_DATE_FORMAT)
    with ui.input(
        placeholder,
        validation={_wrong_format: validate_q_date},
    ).props(
        'outlined'
    ).classes('admin-calendar-container-input') as date_input:
        with ui.menu().props('no-parent-event') as calendar_menu:
            with ui.date(mask='DD-MM-YYYY').bind_value(date_input).props(props) as calendar:
                with ui.row().classes('justify-end'):
                    ui.button(
                        text=_(TKey.A_CLOSE),
                        on_click=calendar_menu.close,
                    ).props('flat')

        with date_input.add_slot('append'):
            ui.icon('edit_calendar').on('click', calendar_menu.open).classes('cursor-pointer')
    date_input.set_value(value)
    return date_input, calendar

#####################################################################################################
