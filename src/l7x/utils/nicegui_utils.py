import asyncio
from collections.abc import Callable
from typing import Final, TypedDict, NotRequired, MutableMapping, Any, AsyncGenerator, Literal

from nicegui import events as _nicegui_events, ui
from nicegui.elements.image import Image
from nicegui.elements.textarea import Textarea

from l7x.db import AudioModel, ConversationModel, TextModel, UserModel
from l7x.services.recognize_service import PrivateRecognizeService
from l7x.services.translation_service import PrivateTranslationService
from l7x.types.language import LKey
from l7x.types.localization import TKey
from l7x.utils.conversation_utils import check_waiting_conversation
from l7x.utils.datetime_utils import now_utc
from l7x.utils.db_utils import SessionClosed, SessionNotFound, UserNotActive, check_valid_session
from l7x.utils.lang_utils import create_available_langs_list
from l7x.utils.orjson_utils import orjson_dumps_to_str
from l7x.utils.storage_utils import ConversationStorageHelper, Conversation

#####################################################################################################

TableColumn = TypedDict('TableColumn', {
    'name': str,
    'label': str,
    'field': str,
    'align': str,
    'sortable': NotRequired[bool],
    ':sort': NotRequired[str],
})

#####################################################################################################

def prepare_session_storage(session_storage) -> MutableMapping[str, Any]:
    clear_storage = {
        'difficulty_of_use_survay': [],
        'recommends_survay': [],
        'translation_quality_survay': [],
        'elements': {},
    }
    session_storage.update(clear_storage)
    return session_storage

#####################################################################################################

class GuiProcessor:
    #####################################################################################################

    def __init__(
        self,
        session_storage,
        session_uuid: str,
        user: UserModel,
        app,
        pages,
    ):
        self.pages = pages
        self.app = app
        self.logger = app.logger
        self.session_uuid = session_uuid
        self.user = user
        self.recognizer: PrivateRecognizeService = app.recognize_service
        self.translator: PrivateTranslationService = app.translation_service
        self.storage = session_storage
        self.generator = None
        self.audio_recorder: AudioRecorder | None = None
        self.active_mic_btn = None
        self.messages: list[TextModel] = []
        self.wait_ico = None
        self.conversation: ConversationModel | None = None
        self.questionare: dict[str, str] = {}
        self.available_langs = None
        self.localized_available_langs = None
        self.langs_directions = None
        self.base_lang = self.app.app_settings.default_language_locale
        self._interlocutor_lang = None
        self.selected_lang: str | None = None
        self.page_container = None
        self.review: TextModel | None = None
        self.global_conv_storage: ConversationStorageHelper = app.conversations_storage
        self._conv_in_storage: Conversation | None = None
        # self.global_conv_storage = self.app.storage.general.get('conversations')
        # self.app.storage.general['conversations'] = {}
        # self.global_conv_storage = self.app.storage.general['conversations']
        # self.global_conv_storage = app.storage.general['conversations'] =
        #####################################################################################################

    @property
    def interlocutor_lang(self):
        return self._interlocutor_lang

    def element(self, element_name):
        return self.storage['elements'].get(element_name)

    #####################################################################################################

    def localize(self, tkey) -> str:
        lkey = LKey(self.selected_lang if self.selected_lang is not None else self.base_lang)
        return tkey(self.logger, lkey)

    #####################################################################################################

    def langs_options(self, direction: Literal['source', 'target'] = 'target') -> dict[str, str]:
        """Для получения списка отображаемых языков на gui (без дефолтного языка)"""
        return self.localized_available_langs
        # displayed_langs_opts = self.localized_available_langs.copy()
        # if direction == 'target':
        #     displayed_langs_opts.pop(self.base_lang, None)
        # elif direction == 'source':
        #     displayed_langs_opts.pop(self.selected_lang, None)
        # return displayed_langs_opts

    #####################################################################################################

    def direction(self) -> str:
        return self.langs_directions.get(self.selected_lang, 'ltr')

    #####################################################################################################

    @staticmethod
    def check_session_exp(handler_func):
        """Декоратор для проверки активности сессии"""
        async def wrapper(self, *args, **kwargs):
            try:
                await check_valid_session(self.session_uuid)
            except (UserNotActive, SessionClosed, SessionNotFound):
                ui.navigate.to('/login')
                return

            return await handler_func(self, *args, **kwargs)
        return wrapper

    #####################################################################################################

    def set_interlocutor_language(self) -> None:
        cur_conv = self.global_conv_storage.get_conv(self.conversation.primary_uuid)
        self._interlocutor_lang = cur_conv.get_interlocutor_lang_by_session(session_id=self.session_uuid)

    #####################################################################################################

    async def _translate(self, text: str) -> str:
        if text == '':
            return ''
        return await self.translator.translate(
            text=text,
            source_lang=self.selected_lang,
            target_lang=self._interlocutor_lang,
        )

    #####################################################################################################

    @check_session_exp
    async def start_mic_record(self) -> None:
        """Начало записи аудио на странице диалога. После остановки записи сработает функция self._create_dialog_msg"""
        mic: Final[Image] = self.element('mic_not_active')
        mic.props(add='disabled')._event_listeners.clear()

        if self.audio_recorder is not None:
            return
        self.audio_recorder = AudioRecorder(on_audio_ready=lambda audio_uuid: self._create_dialog_msg(audio_uuid))
        self.audio_recorder.start_recording()
        self.active_mic_btn = mic
        self.active_mic_btn.set_visibility(False)

    #####################################################################################################

    @check_session_exp
    async def stop_mic_record(self, client: bool = True) -> None:
        """Конец записи на странице диалога."""
        # dialog_background: Final = self.element('dialog_background')
        for session_id in self._conv_in_storage.shared_elements:
            dialog_background = self._conv_in_storage.shared_elements[session_id]['dialog_background']
            if dialog_background.visible:
                print("Hide dialog background")
                dialog_background.set_visibility(False)

        if self.audio_recorder is not None:
            self.audio_recorder.stop_recording()
        if self.active_mic_btn is not None:
            self.active_mic_btn.set_visibility(True)

        with self.element('chat'):  # добавление иконки ожидания при нажатии на микрофон
            # if dialog_background.visible:
            #     dialog_background.set_visibility(False)
            with ui.row().classes('message-container').classes(
                'justify-end' if client else 'justify-start') as self.wait_ico:
                with ui.row().classes('client-spinner-container' if client else 'operator-spinner-container'):
                    ui.element('span').classes('spinner msg-spinner')

    #####################################################################################################

    async def check_interlocutor_messages(self):
        chat: Final = self.element('chat')
        if not chat:
            print('There is no "chat" element')
            return
        if self._conv_in_storage is None:
            return
        interlocutor_session_id = self._conv_in_storage.get_interlocutor_session_id(client_session_id=self.session_uuid)
        with chat:
            while msg := self._conv_in_storage.get_message(interlocutor_session_id):
                print(f'Recieved msg - {msg}')
                await self._add_dialog_msg(msg)
            print('No messages in queue')
    #####################################################################################################

    async def _add_dialog_msg(self, message: TextModel, fixed: bool = False) -> None:
        """
        Функция добавляет сообщение на страницу диалога.
        Если установлен флаг fixed=True, добавится отредактированный текст.
        """
        is_client = str(message.owner_session_uuid.primary_uuid) != self.session_uuid
        client_direction = self.direction()
        text_align = f'text-align:{"right" if client_direction == "rtl" else "left"}'
        with ui.element('div').classes('message-container').style(
            'flex-direction:row-reverse' if is_client else 'flex-direction:row'
        ):
            with ui.element('div').classes('client_msg' if is_client else 'operator_msg'):
                with ui.row():
                    with ui.column().style('width:440px'):
                        or_t = ui.label(
                            text=message.fixed_text if fixed else message.recognized_text,
                        ).style(
                            text_align if is_client else 'text-align:left',
                        ).classes(
                            'original-msg-text'
                        ).props(
                            f'dir="{client_direction}"' if is_client else 'dir="ltr"',
                        )

                        tr_t = ui.label(
                            text=message.translated_text,
                        ).style(
                            'text-align:left' if is_client else text_align,
                        ).classes(
                            'translated-msg-text'
                        ).props(
                            'dir="ltr"' if is_client else f'dir="{client_direction}"',
                        )

                    with ui.column().classes('edit_msg_container h-full items-center'):
                        ui.html(
                            content='<i class="material-icons edit-ico">edit</i>'
                        ).on(
                            type='click',
                            handler=lambda _: self.edit_text(or_t, tr_t, is_client, message),
                        )

    #####################################################################################################

    async def _close_wait_ico(self) -> None:
        """Функция для удаления иконок ожидания при транскрибировании на странице диалога."""
        if self.wait_ico is not None:
            self.wait_ico.delete()
            self.wait_ico = None

    #####################################################################################################

    async def _create_dialog_msg(self, audio_uuid) -> None:
        """Функция обработчик записанного аудио с микрофона на странице диалога."""
        self.audio_recorder = None
        chat: Final = self.element('chat')
        chat_messages: Final = self.element('chat_messages')
        mic: Final[Image] = self.element('mic_not_active')
        dialog_background = self.element('dialog_background')

        async def _deactivate_record(error_msg: bool = False) -> None:
            if error_msg:
                ui.notify(self.localize(TKey.REC_ERROR_MSG), position='top', type='negative')
            mic.props(remove='disabled').on(type='click', handler=self.start_mic_record)
            if not self.messages and not dialog_background.visible:
                dialog_background.set_visibility(True)
            await self._close_wait_ico()
            await asyncio.sleep(0.1)

        if audio_uuid is not None:
            audio_obj = await AudioModel.objects.get_or_none(primary_uuid=audio_uuid)
            if audio_obj is not None:
                wav_audio_file = audio_obj.audio_raw
                source_lang = self.selected_lang
                target_lang = self._interlocutor_lang

                recognized_text = await self.recognizer.recognize(
                    file_name='test.wav', wav=wav_audio_file, language=source_lang
                )

                if not recognized_text:
                    await _deactivate_record(error_msg=True)
                    return

                try:
                    translated_text = await self._translate(text=recognized_text)
                except Exception as ex:
                    self.logger.error(f'Error when translate: {ex}')
                    await _deactivate_record(error_msg=True)
                    return

                message = await TextModel(
                    create_ts=now_utc(),
                    audio_id=audio_uuid,
                    lang_from=source_lang,
                    lang_to=target_lang,
                    recognized_text=recognized_text,
                    translated_text=translated_text,
                    owner_session_uuid=self.session_uuid,
                    conversation_id=self.conversation  # TODO CHECK IF IT WILL WORK
                ).upsert()
                self.messages.append(message)
                # TODO попробовать все меседжи положить в общий список
                self._conv_in_storage.messages.append(message)

                await _deactivate_record()

                with chat:
                    chat_messages.refresh()

                return

        await _deactivate_record(error_msg=True)

    # @ui.refreshable
    # async def chat_messages(self):
    #     print('render messages')
    #     for message in self._conv_in_storage.messages:
    #         # await self._add_dialog_msg(message)
    #         is_client = str(message.owner_session_uuid.primary_uuid) != self.session_uuid
    #         client_direction = self.direction()
    #         ui.chat_message(
    #             text=message.translated_text,
    #             sent=is_client,
    #         )
        # interlocutor_session_id = self._conv_in_storage.get_interlocutor_session_id(client_session_id=self.session_uuid)
        #
        # if self._conv_in_storage.messages.get(interlocutor_session_id):
        #     print('Process interlocutor messages')
        #     for message in self._conv_in_storage.messages[interlocutor_session_id]:
        #         await self._add_dialog_msg(message)
        # if self._conv_in_storage.messages.get(self.session_uuid):
        #     print('Process client messages')
        #     for message in self._conv_in_storage.messages[self.session_uuid]:
        #         await self._add_dialog_msg(message)


    #####################################################################################################

    async def _next_page_generator(self, start_page_index) -> AsyncGenerator:
        for current_page_index in range(start_page_index, len(self.pages)):
            yield await self._set_visible_page(current_page_index)

    #####################################################################################################

    @check_session_exp
    async def next_page(self):
        """Функция для перехода на следующую страницу"""
        if self.generator is not None:
            try:
                await anext(self.generator)
            except StopAsyncIteration:
                await self.init_start_page()

    #####################################################################################################

    async def init_start_page(self, *, start_page_index: int = 0, conversation=None):
        """Инициализация генератора и показ выбранной страницы"""
        self.generator = self._next_page_generator(start_page_index)
        self.selected_lang = None
        self.available_langs, self.langs_directions = await create_available_langs_list(self.app)
        await self.create_localized_available_langs()
        self.messages = []
        self.review = None
        self.questionare = {}
        if conversation is not None:
            # TODO Обрабатываем поведение когда conversation у пользователя уже есть conversation
            self.conversation = conversation
            if not self.global_conv_storage.get_conv(self.conversation.primary_uuid):
                self._conv_in_storage = self.global_conv_storage.create_conv(conv_id=self.conversation.primary_uuid)
                self._conv_in_storage.add_session_to_conv(self.session_uuid)
            else:
                self._conv_in_storage = self.global_conv_storage.get_conv(conv_id=self.conversation.primary_uuid)
        else:
            # TODO Обрабатываем поведение когда у пользователя нет conversation
            conv = await check_waiting_conversation(session_id=self.session_uuid, user_id=self.user.primary_uuid)
            if conv is not None:
                # Когда уже есть conversation на ожидании
                self.conversation = conv
                self.conversation.second_user_session = self.session_uuid
                await self.conversation.upsert()
                self._conv_in_storage = self.global_conv_storage.get_conv(self.conversation.primary_uuid)
                self._conv_in_storage.add_session_to_conv(self.session_uuid)
            else:
                # Когда создаём новый conversation
                self.conversation = await ConversationModel(first_user_session=self.session_uuid).upsert()
                self._conv_in_storage = self.global_conv_storage.create_conv(conv_id=self.conversation.primary_uuid)
                self._conv_in_storage.add_session_to_conv(self.session_uuid)
        if self.storage is not None:
            if self.storage.get('elements'):
                self.storage = prepare_session_storage(self.storage)
        await self.next_page()

    #####################################################################################################

    async def prepare_dialog_lang_selector(self) -> None:
        await self.create_localized_available_langs()
        if lang_selector_target := self.element('client_lang_selector'):
            lang_selector_target.set_options(self.langs_options('target'))
            lang_selector_target.set_value(self.selected_lang)
        if lang_selector_source := self.element('source_lang_select'):
            lang_selector_source.set_options(self.langs_options('source'))

    #####################################################################################################

    @check_session_exp
    async def prepare_radio_lang_selector(self):
        await self.create_localized_available_langs()
        if lang_radio := self.element('lang_radio'):
            lang_radio.set_options(self.langs_options())
            lang_radio.set_value(self.selected_lang)

    #####################################################################################################

    async def restore_conversation(self, conversation: ConversationModel, conv_in_storage: Conversation):
        """Восстановления состояния страницы из данных бд последней беседы из текущей сессии"""
        await self.init_start_page(start_page_index=1, conversation=conversation)
        self._conv_in_storage = conv_in_storage
        self.selected_lang = conv_in_storage.get_selected_lang_by_session(session_id=self.session_uuid)
        await self.prepare_dialog_lang_selector()
        await self.lang_selector_target_handler(self.selected_lang)

        messages = await TextModel.objects.filter(
            conversation_id__primary_uuid=self.conversation.primary_uuid,
        ).order_by( # .exclude(type='feedback')
            'create_ts'
        ).all()

        if messages:
            self.element('dialog_background').set_visibility(False)
            with self.element('chat'):
                self.element('chat_messages').refresh()
                # for message in messages:
                #     self.messages.append(message)
                #     await self._add_dialog_msg(message, fixed=(message.edit_ts != None))

    #####################################################################################################

    @check_session_exp
    async def create_localized_available_langs(self):
        self.localized_available_langs = {}
        for code, en_lang_name in self.available_langs.items():
            tkey = TKey[f'T_{en_lang_name.upper()}']
            orig_name = tkey(self.logger, LKey(code)).strip().title()
            if self.selected_lang is not None:
                localized_lang_name = tkey(self.logger, LKey(self.selected_lang)).strip().title()
            else:
                localized_lang_name = tkey(self.logger, LKey(self.base_lang)).strip().title()
            if localized_lang_name == orig_name:
                self.localized_available_langs[code] = orig_name
            else:
                self.localized_available_langs[code] = f'{localized_lang_name} ({orig_name})'
    #####################################################################################################

    @check_session_exp
    async def select_lang_radio_handler(self, lang):
        self.selected_lang = lang
        self.element('select_lang_title').set_text(self.localize(TKey.LANG_SELECT_TITLE))
        self.element('confirm_lang_button').set_text(self.localize(TKey.START_DIALOG))
        self.storage['end_dialog_label'].set_text(self.localize(TKey.END_DIALOG))
        await self.prepare_radio_lang_selector()

    #####################################################################################################

    @check_session_exp
    async def save_lang_and_next_page(self):
        await self.set_new_lang(self.selected_lang)
        await self.next_page()

    #####################################################################################################

    async def lang_selector_source_handler(self, lang: str) -> None:
        if lang == self.selected_lang:
            self.logger.warning('Impossible to select the same source language as in the target select.')
            return
        self.base_lang = lang
        if lang_selector := self.element('client_lang_selector'):
            lang_selector.set_options(self.langs_options(direction='target'))

    #####################################################################################################

    @check_session_exp
    async def lang_selector_target_handler(self, lang) -> None:
        await self.set_new_lang(lang)
        self.element('dialog_placeholder').set_text(self.localize(TKey.DIALOG_PLACEHOLDER))
        self.storage['end_dialog_label'].set_text(self.localize(TKey.END_DIALOG))
        await self.prepare_dialog_lang_selector()

    #####################################################################################################

    @check_session_exp
    async def set_new_lang(self, lang):
        """Устанавливает язык в селекторе на странице диалога"""
        self.selected_lang = lang
        self.global_conv_storage.handle_select_lang(
            conv_id=self.conversation.primary_uuid,
            session_id=self.session_uuid,
            lang=lang,
        )
        # await self.conversation.upsert(selected_lang=self.selected_lang)

    #####################################################################################################

    async def _set_visible_page(self, visible_page_index):
        """открывает страницу с выбранным индексом"""
        page_func = self.pages[visible_page_index]
        self.page_container.clear()
        with self.page_container:
            await page_func(self, self.storage)

        self.storage['close_dialog_btn'].set_visibility(visible_page_index == 1)

    #####################################################################################################

    @check_session_exp
    async def select_element(
        self,
        selected_element,
        survay_name,
    ):
        """Выделение и запись элементов в голосовалках"""
        sender_element: Final = selected_element.sender
        self.questionare[survay_name] = sender_element.text
        survay_elems = self.storage[f'{survay_name}_survay']
        button = self.element(f'{survay_name}_next_btn')

        for element, text in survay_elems:
            if element != sender_element:
                element.classes(remove='selected-q')
                text.classes(remove='vote-selected-text')
            else:
                element.classes(add='selected-q')
                text.classes(add='vote-selected-text')

        if not button.enabled:
            button.set_enabled(True)

    #####################################################################################################

    @check_session_exp
    async def close_dialog_btn_handler(self):
        """Создание модалки закрытия диалога"""
        async def finish_work():
            close_popup.close()
            if self.app.app_settings.enable_questionnaire:
                await self.next_page()
            else:
                await self.close_conv_and_next()

        with ui.dialog().classes('close-dialog') as close_popup:
            with ui.column().classes('close-dialog-popup-container'):
                with ui.row().classes('popup-close-ico-container'):
                    ui.image('/static/images/close.svg').on('click', close_popup.close)
                ui.label(text=self.localize(TKey.CLOSE_POPUP_TITLE)).classes('close-dialog-modal-orig')
                ui.label(text=self.localize(TKey.CLOSE_POPUP_TEXT)).classes('close-dialog-modal-translate')
                with ui.row():
                    ui.button(text=self.localize(TKey.CLOSE_POPUP_END_BTN), on_click=finish_work).classes('close-dialog-confirm-btn')
                    ui.button(text=self.localize(TKey.CLOSE_POPUP_CONTINUE_BTN), on_click=close_popup.close).classes('close-dialog-return-btn')
        close_popup.open()

    #####################################################################################################

    @check_session_exp
    async def edit_text(self, text_elem, translated_elem, client, text: TextModel):
        """Функция редактирования сообщений."""
        if text is None:
            self.logger.warning('Edit text object is None')
            return
        async def set_new_text():
            corrected_text = pop_up_input.value
            translated_corrected_text = await self._translate(corrected_text, client=client)

            await text.upsert(
                fixed_text=corrected_text,
                translated_text=translated_corrected_text,
                edit_ts=now_utc(),
            )

            if isinstance(text_elem, Textarea):
                text_elem.set_value(corrected_text)
            else:
                text_elem.set_text(corrected_text)
            if isinstance(translated_elem, Textarea):
                translated_elem.set_value(translated_corrected_text)
            else:
                translated_elem.set_text(translated_corrected_text)
            dialog.close()
            await asyncio.sleep(0.2)

        orig_text = text_elem.value if isinstance(text_elem, Textarea) else text_elem.text
        direction = self.direction()

        with ui.dialog().classes('w-full') as dialog:
            with ui.row().classes('w-full popup-edit-container shadow-line'):
                with ui.column().style('width:90%'):
                    ui.label(text=self.localize(TKey.EDITING)).classes('w-full').style('font-size:16px')
                    pop_up_input = ui.input(
                        value=orig_text,
                    ).style(
                        f'text-align:{"right" if direction == "rtl" else "left"}' if client else 'text-align:left',
                    ).classes(
                        'w-full edit-input'
                    ).props(
                        'autofocus standout="bg-grey-12 text-black',
                    ).props(
                        add=f'dir="{direction}"' if client else 'dir="ltr"',
                    )

                with ui.column().classes('items-center'):
                    ui.html(
                        content='<div class="close-ico-wrap"><i class="material-icons close-ico">close</i></div>',
                    ).on(
                        type='click',
                        handler=dialog.close,
                    )
                    ui.html(
                        content='<div class="apply-ico-wrap"><i class="material-icons apply-ico">check</i></div>',
                    ).on(
                        type='click',
                        handler=set_new_text,
                    )
        dialog.open()

    #####################################################################################################

    @check_session_exp
    async def input_text(self, text_elem, translated_elem):
        """Функция ввода отзыва. Создаёт модалку для ввода текста."""
        async def set_new_text():
            input_text = pop_up_input.value
            translated_input_text = await self._translate(input_text, client=True)

            self.review = await TextModel(
                create_ts=now_utc(),
                lang_from=self.selected_lang,
                lang_to=self.base_lang,
                recognized_text=input_text,
                translated_text=translated_input_text,
                type='feedback',
                conversation_id=self.conversation.primary_uuid
            ).upsert()

            if isinstance(text_elem, Textarea):
                text_elem.set_value(input_text)
            else:
                text_elem.set_text(input_text)
            if isinstance(translated_elem, Textarea):
                translated_elem.set_value(translated_input_text)
            else:
                translated_elem.set_text(translated_input_text)
            dialog.close()
            await asyncio.sleep(0.2)

        direction: Final = self.direction()

        orig_text = text_elem.value if isinstance(text_elem, Textarea) else text_elem.text
        with ui.dialog() as dialog:
            with ui.row().classes('review-window-input'):
                with ui.column().style('width:90%').classes('h-full'):
                    pop_up_input = ui.textarea(
                        value=orig_text,
                    ).style(
                        f'text-align:{"right" if direction == "rtl" else "left"}',
                    ).classes(
                        'w-full h-full',
                    ).props(
                        f'autofocus outlined dir="{direction}"',
                    )
                with ui.column().classes('items-center h-full'):
                    ui.html(
                        content='<div class="apply-ico-wrap"><i class="material-icons apply-ico">check</i></div>',
                    ).on(
                        type='click',
                        handler=set_new_text,
                    ).classes(
                        'input-text',
                    )
        dialog.open()

    #####################################################################################################

    async def _add_review_msg(self, audio_uuid: str | None):
        """Обработчик записанного аудио на странице отзыва"""
        review_orig_text_element = self.element('review_orig_text')
        review_translated_text_element = self.element('review_translated_text')

        async def _deactivate_review_record(error_msg: bool = False):
            if error_msg:
                ui.notify(self.localize(TKey.REC_ERROR_MSG), position='top', type='negative')
            self.element('submit_button').set_enabled(True)
            self.element('review_spinner').set_visibility(False)
            self.element('review_not_active_mic').props(remove='disabled').on('click', self.start_review_recognize)

        if audio_uuid is not None:
            audio_obj = await AudioModel.objects.get_or_none(primary_uuid=audio_uuid)
            if audio_obj is not None:
                wav_audio_file = audio_obj.audio_raw

                recognized_review_text = await self.recognizer.recognize(
                    file_name='test.wav',
                    wav=wav_audio_file,
                    language=self.selected_lang,
                )

                if not recognized_review_text:
                    await _deactivate_review_record(error_msg=True)
                    return

                translated_review_text: Final = await self._translate(recognized_review_text, client=True)

                self.review = await TextModel(
                    create_ts=now_utc(),
                    audio_id=audio_uuid,
                    lang_from=self.selected_lang,
                    lang_to=self.base_lang,
                    recognized_text=recognized_review_text,
                    translated_text=translated_review_text,
                    type='feedback',
                    conversation_id=self.conversation.primary_uuid
                ).upsert()

                review_orig_text_element.props(add=f'dir="{self.direction()}"')
                review_orig_text_element.set_text(self.review.recognized_text)
                review_translated_text_element.set_text(self.review.translated_text)
                await _deactivate_review_record()
                return

        await _deactivate_review_record(error_msg=True)

    #####################################################################################################

    @check_session_exp
    async def start_review_recognize(self):
        self.audio_recorder = AudioRecorder(on_audio_ready=self._add_review_msg)
        self.audio_recorder.start_recording()
        review_mic: Final = self.element('review_not_active_mic')
        review_mic.props(add='disabled')._event_listeners.clear()

        self.element('review_orig_text').set_text('')
        self.element('review_translated_text').set_text('')
        self.element('review_not_active_mic').set_visibility(False)
        self.element('submit_button').set_enabled(False)

    #####################################################################################################

    @check_session_exp
    async def stop_review_recognize(self):
        if self.audio_recorder is not None:
            self.audio_recorder.stop_recording()
            self.audio_recorder = None
        self.element('review_not_active_mic').set_visibility(True)
        self.element('review_spinner').set_visibility(True)

#####################################################################################################

    @check_session_exp
    async def close_conv_and_next(self):
        self.conversation.end_ts = now_utc()
        if self.questionare:
            self.conversation.questionare = orjson_dumps_to_str(self.questionare)
        await self.conversation.update()
        await self.next_page()

#####################################################################################################

class AudioRecorder(ui.element, component='audio_recorder.vue'):
    #####################################################################################################

    def __init__(self, *, on_audio_ready: Callable | None = None) -> None:
        super().__init__()
        self.mime_type: Final = 'audio/wav'

        async def handle_audio(e: _nicegui_events.GenericEventArguments) -> None:
            if on_audio_ready:
                await on_audio_ready(e.args.get('audio_uuid'))
        self.on('audio_ready', handle_audio)

    #####################################################################################################

    def start_recording(self) -> None:
        self.run_method('startRecording')

    #####################################################################################################

    def stop_recording(self) -> None:
        self.run_method('stopRecording')

    #####################################################################################################
