#####################################################################################################
from typing import Final

from nicegui import ui
from nicegui.observables import ObservableDict

from l7x.db import ConversationModel, UserModel
from l7x.types.localization import TKey
from l7x.utils.nicegui_utils import GuiProcessor
from l7x.utils.storage_utils import Conversation

#####################################################################################################

CLIENTS_CONNECTED = 0
SPINNER = None

async def header_gui(gp: GuiProcessor, storage: ObservableDict) -> None:
    with ui.row().classes('head-container'):
        ui.image('/static/images/logo_main.svg').classes('company-logo')
        with ui.row().classes(
            'dialog-close-btn-container',
        ).on(
            type='click',
            handler=gp.close_dialog_btn_handler,
        ) as close_dialog_btn:
            with ui.column().classes('dialog-close-icon-btn-container'):
                ui.html('<i class="material-icons">close</i>').classes('dialog-close-icon-btn')
            with ui.column().classes('justify-center items-center').style('gap:2px;width:70%'):
                end_dialog_label = ui.label(gp.localize(TKey.END_DIALOG)).classes('dialog-close-translated-txt')
                ui.label(gp.localize(TKey.END_DIALOG)).classes('dialog-close-orig-txt')

    storage['close_dialog_btn'] = close_dialog_btn
    storage['end_dialog_label'] = end_dialog_label

#####################################################################################################

async def select_lang_page_gui(gp: GuiProcessor, storage: ObservableDict):

    with ui.column().classes('main-block-container'):
        select_lang_title = ui.label(gp.localize(TKey.LANG_SELECT_TITLE)).classes('font-bold text-3xl')
        lang_radio = ui.radio(
            options=gp.langs_options(),
            on_change=lambda e: gp.select_lang_radio_handler(e.value),
        ).classes('radio-align').props('dir="auto"')

    with ui.column().classes('footer-container'):
        confirm_lang_button = ui.button(
            text=gp.localize(TKey.START_DIALOG),
            on_click=gp.save_lang_and_next_page,
        ).classes('next-btn')
        confirm_lang_button.bind_enabled_from(
            gp,
            target_name='selected_lang',
            backward=lambda x: (x is not None),
        )
    conversation_number = 'second' if gp.conversation.second_user_session else 'first'

    ui.notify(f'You are connected as a {conversation_number}')
    storage['elements'].update({
        'lang_radio': lang_radio,
        'select_lang_title': select_lang_title,
        'confirm_lang_button': confirm_lang_button,
    })

    d = True

#####################################################################################################

# async def waiting_conversation_page_gui(gp: GuiProcessor, storage: ObservableDict):
#
#     async def conv_polling():
#         conv_uuid = gp.conversation.primary_uuid
#         conv = await ConversationModel.objects.get(primary_uuid=conv_uuid)
#         if conv.end_ts is not None:
#             ui.notify('Conversation was ended')
#             spinner.set_visibility(False)
#             waiting_card.set_visibility(False)
#             timer.cancel()
#             return
#         if conv.second_user_session is not None:
#             ui.notify('Second client connected')
#             spinner.set_visibility(False)
#             waiting_card.set_visibility(False)
#             timer.cancel()
#
#     if not gp.conversation.second_user_session:
#         with ui.card().classes('justify-center').tailwind.width('full').height('full') as waiting_card:
#             ui.label('Waiting for the second client')
#             spinner = ui.spinner()
#
#         timer = ui.timer(3.0, conv_polling)

    # await gp.next_page()
def invert_visibility(x: bool):
    return not x

@ui.refreshable
async def chat_messages(gp, conv):
    print('render messages')
    for message in conv.messages:
        # await self._add_dialog_msg(message)
        is_client = str(message.owner_session_uuid.primary_uuid) != gp.session_uuid
        ui.chat_message(
            text=message.translated_text,
            sent=is_client,
        )


async def dialog_page_gui(gp: GuiProcessor, storage: ObservableDict):

    async def conv_polling():
        if cur_conversation and cur_conversation.is_ready_to_start():
            gp.set_interlocutor_language()
            ui.notify('Second client connected')
            spinner.set_visibility(False)
            waiting_card.set_visibility(False)
            timer.cancel()

    conv_id = str(gp.conversation.primary_uuid)
    cur_conversation: Conversation = gp.global_conv_storage.get_conv(conv_id)
    cur_user: Final[UserModel] = gp.user
    user_direction_in_conv = cur_conversation.get_direction_by_session(gp.session_uuid)

    with ui.column().classes('main-block-container'):

        with ui.card().classes('justify-center') as waiting_card:
            waiting_card.tailwind.width('full').height('full')
            ui.label('Waiting for the second client')
            ui.label(f'Current conversation: {cur_conversation.conv_id}')
            ui.label(f'First user: {cur_conversation.first_user_session}')
            spinner = ui.spinner()
            timer = ui.timer(3.0, conv_polling)

        with ui.element('div').classes('centered-container') as dialog_background:
            ui.image('/static/images/mic.svg').style('width:71px;height:71px')
            dialog_placeholder = ui.label(
                text=gp.localize(TKey.DIALOG_PLACEHOLDER),
            ).style(
                'width:394px; height:86px',
            ).classes(
                'background-text',
            )
        with ui.element('div').classes('w-full chat-window'):
            chat = ui.element('div').classes(
                'w-full chat-container',
            ).bind_visibility_from(
                target_object=dialog_background,
                value=False,
            )
            with chat:
                await chat_messages(gp, cur_conversation)

            # ui.timer(5, callback=gp.check_interlocutor_messages)
    ui.column().classes('footer-container shadow-line')

    with ui.row().classes('mics-container').bind_visibility_from(waiting_card, backward=invert_visibility):
        with ui.column().classes('start-mic-block'):
            with ui.row().classes('justify-center'):
                mic_not_active = ui.image(
                    '/static/images/blue-mic.svg',
                ).classes(
                    'blue-mic',
                ).on(
                    type='click',
                    handler=gp.start_mic_record,
                )

                mic_active = ui.image(
                    '/static/images/record.svg',
                ).classes(
                    'blue-mic',
                ).bind_visibility_from(
                    target_object=mic_not_active,
                    value=False,
                ).on(
                    type='click',
                    handler=lambda _: gp.stop_mic_record(client=False),
                )
                if not gp.app.app_settings.enable_base_lang_select:
                    ui.label(text=gp.localized_available_langs.get(gp.selected_lang)).classes('mic-lang-text w-full')
                else:
                    source_lang_select = ui.select(
                        options=gp.langs_options('source'),
                        on_change=lambda e: gp.lang_selector_source_handler(e.value),
                    ).classes(
                        'mic-lang-selector',
                    ).props(
                        'rounded standout v-model="model" dir="auto"',
                    ).bind_value_from(
                        target_object=gp,
                        target_name='base_lang'
                    )
                    storage['elements'].update({
                        'source_lang_select': source_lang_select
                    })
                mic_active.set_visibility(False)

        with ui.column().classes('start-mic-block'):
            with ui.row().classes('justify-center gap-0'):
                ui.label(text=f'You are the {user_direction_in_conv} in conversation').classes('mt-4 text-zinc-500')
                ui.label().classes('mt-4 text-zinc-500').bind_text_from(gp, target_name='selected_lang',
                                                                        backward=lambda x: f"Your selected lang is {x}")
                ui.label().classes('mt-4 text-zinc-500').bind_text_from(gp, target_name='interlocutor_lang',
                                                                        backward=lambda
                                                                            x: f"Interlocutor selected lang is {x}")
                ui.label(text=f'Current user: {cur_user.full_name}').classes('mt-4 text-zinc-500')

    cur_conversation.add_elem(str(gp.session_uuid), 'dialog_background', dialog_background)
    # cur_conversation.shared_elements[str(gp.session_uuid)]['dialog_background'] = dialog_background
    # cur_conversation.shared_elements['dialog_placeholder'] = dialog_placeholder

    storage['elements'].update({
        'dialog_background': dialog_background,
        'dialog_placeholder': dialog_placeholder,
        'chat': chat,
        'chat_messages': chat_messages,
        'mic_not_active': mic_not_active,
    })

#####################################################################################################

async def use_translator_survay_page_gui(gp: GuiProcessor, storage: ObservableDict):
    survay_labels = [
        gp.localize(TKey.SURVAY_ONE_RATE_ONE),
        gp.localize(TKey.SURVAY_ONE_RATE_TWO),
        gp.localize(TKey.SURVAY_ONE_RATE_THREE),
        gp.localize(TKey.SURVAY_ONE_RATE_FOUR),
        gp.localize(TKey.SURVAY_ONE_RATE_FIVE),
    ]

    with ui.column().classes('main-block-container vote-container'):
        with ui.column().classes('items-center'):
            ui.label(text=f'{gp.localize(TKey.QUESTION)} 1 {gp.localize(TKey.OF)} 4').classes('questions-counter-text')
            ui.label(gp.localize(TKey.SURVAY_ONE_TITLE)).classes('questions-title')

        with ui.row().classes('votes-blocks'):
            for number, difficult_desc in zip(range(1, 6), survay_labels):
                with ui.column().classes('items-center gap-5'):
                    difficulty_of_use_score = ui.label(
                        text=str(number),
                    ).classes(
                        'vote unselected-q',
                    ).on(
                        type='click',
                        handler=lambda selected_vote: gp.select_element(selected_vote, 'difficulty_of_use'),
                    )
                    difficulty_of_use_text = ui.label(text=difficult_desc).classes('vote-text')
                    storage['difficulty_of_use_survay'].append((difficulty_of_use_score, difficulty_of_use_text))

    with ui.column().classes('footer-container'):
        difficulty_of_use_next_btn = ui.button(
            text=gp.localize(TKey.NEXT_SURVAY_BTN),
            on_click=gp.next_page,
        ).classes(
            'next-btn',
        )
        ui.label(text=gp.localize(TKey.SKIP_SURVAY_BTN)).classes('skip-btn').on('click', gp.next_page)
        difficulty_of_use_next_btn.set_enabled(False)
    storage['elements'].update({
        'difficulty_of_use_next_btn': difficulty_of_use_next_btn,
    })

#####################################################################################################

async def recommendation_survay_page_gui(gp: GuiProcessor, storage: ObservableDict):
    survay_labels = [
        gp.localize(TKey.SURVAY_TWO_RATE_ONE),
        gp.localize(TKey.SURVAY_TWO_RATE_TWO),
        gp.localize(TKey.SURVAY_TWO_RATE_THREE),
        gp.localize(TKey.SURVAY_TWO_RATE_FOUR),
        gp.localize(TKey.SURVAY_TWO_RATE_FIVE),
    ]

    with ui.column().classes('main-block-container vote-container'):
        with ui.column().classes('items-center'):
            ui.label(text=f'{gp.localize(TKey.QUESTION)} 2 {gp.localize(TKey.OF)} 4').classes('questions-counter-text')
            ui.label(gp.localize(TKey.SURVAY_TWO_TITLE)).classes('questions-title')

        with ui.row().classes('votes-blocks'):
            for number, rec_desc in zip(range(1, 6), survay_labels):
                with ui.column().classes('items-center gap-5'):
                    recommends_score = ui.label(
                        text=str(number)
                    ).classes(
                        'vote unselected-q '
                    ).on(
                        'click',
                        lambda selected_vote: gp.select_element(selected_vote, 'recommends')
                    )
                    recommends_text = ui.label(text=rec_desc).classes('vote-text')
                    storage['recommends_survay'].append((recommends_score, recommends_text))

    with ui.column().classes('footer-container'):
        recommends_next_btn = ui.button(
            text=gp.localize(TKey.NEXT_SURVAY_BTN),
            on_click=gp.next_page,
        ).classes('next-btn')
        ui.label(text=gp.localize(TKey.SKIP_SURVAY_BTN)).classes('skip-btn').on('click', gp.next_page)
        recommends_next_btn.set_enabled(False)
    storage['elements'].update({
        'recommends_next_btn': recommends_next_btn,
    })

#####################################################################################################

async def translation_quality_survay_page_gui(gp: GuiProcessor, storage: ObservableDict):
    survay_labels = [
        gp.localize(TKey.SURVAY_THREE_RATE_ONE),
        gp.localize(TKey.SURVAY_THREE_RATE_TWO),
        gp.localize(TKey.SURVAY_THREE_RATE_THREE),
        gp.localize(TKey.SURVAY_THREE_RATE_FOUR),
        gp.localize(TKey.SURVAY_THREE_RATE_FIVE),
    ]

    with ui.column().classes('main-block-container vote-container'):
        with ui.column().classes('items-center'):
            ui.label(text=f'{gp.localize(TKey.QUESTION)} 3 {gp.localize(TKey.OF)} 4').classes('questions-counter-text')
            ui.label(gp.localize(TKey.SURVAY_THREE_TITLE)).classes('questions-title')

        with ui.row().classes('votes-blocks'):
            for number, rec_desc in zip(range(1, 6), survay_labels):
                with ui.column().classes('items-center gap-5'):
                    translation_quality_score = ui.label(
                        text=str(number)
                    ).classes(
                        'vote unselected-q '
                    ).on(
                        'click',
                        lambda selected_vote: gp.select_element(selected_vote, 'translation_quality')
                    )
                    translation_quality_text = ui.label(text=rec_desc).classes('vote-text')
                    storage['translation_quality_survay'].append((translation_quality_score, translation_quality_text))

    with ui.column().classes('footer-container'):
        translation_quality_next_btn = ui.button(
            text=gp.localize(TKey.NEXT_SURVAY_BTN),
            on_click=gp.next_page,
        ).classes('next-btn')
        ui.label(text=gp.localize(TKey.SKIP_SURVAY_BTN)).classes('skip-btn').on('click', gp.next_page)
        translation_quality_next_btn.set_enabled(False)
    storage['elements'].update({
        'translation_quality_next_btn': translation_quality_next_btn,
    })

#####################################################################################################

async def review_page_gui(gp: GuiProcessor, storage: ObservableDict):
    direction: Final = gp.direction()
    with (ui.column().classes('main-block-container review-container')):
        with ui.column().classes('items-center'):
            ui.label(text=f'{gp.localize(TKey.QUESTION)} 4 {gp.localize(TKey.OF)} 4').classes('questions-counter-text')
            ui.label(gp.localize(TKey.REVIEW_TITLE)).classes('questions-title')

        with ui.row().classes('review-window'):
            review_placeholder = ui.label(gp.localize(TKey.REVIEW_PLACEHOLDER)).classes(
                'review_placeholder',
            ).props(
                f'dir="{direction}"',
            ).style(
                f'text-align:{"right" if direction == "rtl" else "left"}',
            )
            review_spinner = ui.element('span').classes('spinner review-spinner')
            review_spinner.set_visibility(False)
            with ui.column().classes('review-textarea-block').on('click', lambda _: gp.input_text(review_orig_text, review_translated_text)):
                review_orig_text = ui.label().classes('original-msg-text')
                review_translated_text = ui.label().classes('translated-msg-text')

            with ui.column().classes('review-btn-block'):

                with ui.column().style('height:32px width: 100%'):
                    review_edit_btn = ui.html(
                        '<i class="material-icons edit-ico">edit</i>'
                    ).style(
                        'font-size:32px'
                    ).bind_visibility_from(
                        review_orig_text, target_name='text', backward=lambda x: x != ''
                    ).bind_visibility_to(
                        review_placeholder, forward=lambda x: not x
                    ).on(
                        type='click',
                        handler=lambda _: gp.edit_text(
                            review_orig_text,
                            review_translated_text,
                            client=True,
                            text=gp.review,
                        ),
                    )

                review_not_active_mic = ui.image(
                    '/static/images/blue-mic.svg'
                ).classes(
                    'little-blue-mic'
                ).on(
                    'click',
                    gp.start_review_recognize,
                )

                review_active_mic = ui.image(
                    '/static/images/record.svg'
                ).classes(
                    'little-blue-mic'
                ).bind_visibility_from(
                    review_not_active_mic,
                    value=False,
                ).on(
                    'click',
                    gp.stop_review_recognize,
                )

                review_active_mic.set_visibility(False)

    with ui.column().classes('footer-container'):
        submit_button = ui.button(
            text=gp.localize(TKey.FINISH_SURVAY_BTN),
            on_click=gp.close_conv_and_next,
        ).classes('next-btn')
        ui.label(gp.localize(TKey.REVIEW_BOTTOM_TEXT)).classes('skip-review-text')
    storage['elements'].update({
        'submit_button': submit_button,
        'review_not_active_mic': review_not_active_mic,
        'review_edit_btn': review_edit_btn,
        'review_orig_text': review_orig_text,
        'review_translated_text': review_translated_text,
        'review_spinner': review_spinner,
    })

#####################################################################################################

async def final_page_gui(gp: GuiProcessor, storage: ObservableDict):
    with ui.column().classes('main-block-container items-center justify-center'):
        with ui.column().classes('items-center justify-center'):
            with ui.row().classes('finish-checkbox-container'):
                ui.image('/static/images/checked.svg')
            ui.label(gp.localize(TKey.FINAL_TEXT)).classes('questions-title')

    with ui.column().classes('footer-container'):
        ui.button(text=gp.localize(TKey.BACK_TO_MENU_BTN), on_click=gp.next_page).classes('next-btn')

#####################################################################################################
