#####################################################################################################

from fastapi import Request
from nicegui import ui

from l7x.types.language import LKey
from l7x.types.localization import TKey
from l7x.utils.fastapi_utils import AppFastAPI

#####################################################################################################

async def _login_page(request: Request):
    ################### LOAD JS AND CSS ##################
    app = request.app
    default_lang = app.app_settings.default_language_locale

    login_label = TKey.LOGIN(app.logger, LKey(default_lang))
    password_text = TKey.PASSWORD(app.logger, LKey(default_lang))
    sign_in_label = TKey.SIGN_IN(app.logger, LKey(default_lang))

    ui.add_head_html('<link rel="stylesheet" href="./static/style.css">')
    ui.add_body_html('<script src="./static/login_script.js"></script>')

    ####################### HEADER #######################

    with ui.row().classes('head-container'):
        ui.image('/static/images/logo_main.svg').classes('company-logo')

    ####################### LOGIN #######################

    with ui.column().classes(
        'w-full h-full items-center'
    ).style(
        'margin-top:18vh'
    ):
        with ui.column().classes('my-page-container'):
            ui.label(TKey.LOGIN_TO_YOUR_ACCOUNT(app.logger, LKey(default_lang))).classes('questions-title')
            ui.column().classes('login-form-container')
    ui.add_body_html(f"""
        <script>
            document.addEventListener("DOMContentLoaded", () => {{
                displayLoginForm(`{login_label}`, `{password_text}`, `{sign_in_label}`)
            }})
        </script>
    """)

#####################################################################################################

def login_page_listener_registrar(app: AppFastAPI, /) -> None:
    ui.page('/login', response_timeout=30)(_login_page)

#####################################################################################################
