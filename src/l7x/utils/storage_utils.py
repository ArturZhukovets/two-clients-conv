from dataclasses import asdict, dataclass, field
from uuid import UUID

from nicegui import App

from l7x.db import TextModel


@dataclass(kw_only=True)
class Conversation:
    conv_id: str = None

    first_user_session: str = None
    first_user_lang: str = None

    second_user_session: str = None
    second_user_lang: str = None

    messages: list = field(default_factory=list)
    shared_elements: dict = field(default_factory=dict)
    # messages_first_user: list = field(default_factory=list)
    # messages_second_user: list = field(default_factory=list)

    def add_elem(self, session_id: str, name: str, element):
        session_elements = self.shared_elements.get(session_id)
        if session_elements is None:
            self.shared_elements[session_id] = {name: element}
            return
        session_elements[name] = element

    def add_session_to_conv(self, session_id: str) -> None:
        if not self.first_user_session:
            self.first_user_session = session_id
        elif not self.second_user_session:
            self.second_user_session = session_id
        else:
            raise ValueError('Conversation already has two users')

    def set_user_lang(self, lang: str, session_id: str) -> None:
        match session_id:
            case self.first_user_session:
                self.first_user_lang = lang
            case self.second_user_session:
                self.second_user_lang = lang
            case _:
                raise ValueError(f'There are no such session in current conversation "{session_id}"')

    def get_interlocutor_lang_by_session(self, session_id: str) -> str:
        """Отдаёт выбранный собеседником язык"""
        match session_id:
            case self.first_user_session:
                return self.second_user_lang
            case self.second_user_session:
                return self.first_user_lang

    def get_selected_lang_by_session(self, session_id: str) -> str | None:
        match session_id:
            case self.first_user_session:
                return self.first_user_lang
            case self.second_user_session:
                return self.second_user_lang

    def is_ready_to_start(self) -> bool:
        """Ready, когда в conversation есть два пользователя с выбранным языком"""

        return all(
            (
                self.first_user_session,
                self.second_user_session,
                self.first_user_lang,
                self.second_user_lang,
            )
        )

    def add_message(self, session_id: str, message: TextModel) -> None:
        if self.messages.get(session_id) is not None:
            self.messages[session_id].append(message)
        else:
            self.messages[session_id] = [message]

    def get_message(self, session_id: str) -> TextModel | None:
        if self.messages.get(session_id):
            return self.messages[session_id].pop()

    def get_interlocutor_session_id(self, client_session_id: str) -> str:
        match client_session_id:
            case self.first_user_session:
                return self.second_user_session
            case self.second_user_session:
                return self.first_user_session

    def get_direction_by_session(self, session_id: str) -> str | None:
        match session_id:
            case self.first_user_session:
                return 'First'
            case self.second_user_session:
                return 'Second'
            case _:
                return None

class ConversationStorageHelper():
    def __init__(self, app: App):
        app.storage.general['conversations'] = {}
        self._storage = app.storage.general['conversations']

    def create_conv(self, conv_id: str | UUID) -> Conversation:
        if isinstance(conv_id, UUID):
            conv_id = str(conv_id)
        conv = Conversation(conv_id=conv_id)
        self._storage[conv_id] = conv
        return conv

    def get_conv(self, conv_id: str | UUID) -> Conversation | None:
        if isinstance(conv_id, UUID):
            conv_id = str(conv_id)
        return self._storage.get(conv_id)

    def handle_select_lang(self, conv_id: str | UUID, session_id: str | UUID, lang: str) -> None:
        """Find the cur conversation and set selected language for desired session"""
        if isinstance(session_id, UUID):
            session_id = str(session_id)
        conv = self.get_conv(conv_id=conv_id)
        assert conv is not None
        conv.set_user_lang(lang=lang, session_id=session_id)

    def to_dict(self) -> dict:
        ret = {}
        for conv in self._storage:
            ret[conv] = asdict(self._storage[conv])
        return ret

    @property
    def display_conversations(self):
        return self.to_dict()
