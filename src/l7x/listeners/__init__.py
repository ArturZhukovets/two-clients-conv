#####################################################################################################

from collections.abc import Callable, Iterable
from typing import Final, TypeAlias

from l7x.app import App
from l7x.listeners.admin_listener import admin_page_listener_registrar
from l7x.listeners.audio_file_listener import audio_file_page_listener_registrar
from l7x.listeners.authorization_listener import authorization_page_listener_registrar
from l7x.listeners.conversation_data_listener import conversation_data_page_listener_registrar
from l7x.listeners.login_listener import login_page_listener_registrar
from l7x.listeners.mainpage_listener import mainpage_listener_registrar
from l7x.listeners.save_blobs_listener import save_blob_page_listener_registrar
from l7x.listeners.session_exp_listener import session_exp_check_page_listener_registrar
from l7x.listeners.text_data_listener import text_data_page_listener_registrar

#####################################################################################################

ListenersRegistrars: TypeAlias = Iterable[Callable[[App], None]]

#####################################################################################################

def _get_app_listeners_registrars() -> ListenersRegistrars:
    return [
        mainpage_listener_registrar,
        login_page_listener_registrar,
        authorization_page_listener_registrar,
        session_exp_check_page_listener_registrar,
        save_blob_page_listener_registrar,
        admin_page_listener_registrar,
        conversation_data_page_listener_registrar,
        text_data_page_listener_registrar,
        audio_file_page_listener_registrar,
    ]

#####################################################################################################

APP_LISTENERS_REGISTRARS: Final[ListenersRegistrars] = tuple(_get_app_listeners_registrars())

#####################################################################################################
