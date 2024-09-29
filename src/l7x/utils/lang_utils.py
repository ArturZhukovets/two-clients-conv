from collections.abc import Mapping
from logging import Logger
from typing import Final, Callable

from nicegui.language import Language
from nicegui import app as nicegui_app

from l7x.app import App
from l7x.types.lang_services import LanguageDetail
from l7x.types.language import LKey
from l7x.types.localization import TKey

_AVAILABLE_NICEGUI_LOCALES: Final[set] = {
    'ar',
    'ar-TN',
    'az-Latn',
    'bg',
    'bn',
    'ca',
    'cs',
    'da',
    'de',
    'el',
    'en-GB',
    'en-US',
    'eo',
    'es',
    'et',
    'eu',
    'fa',
    'fa-IR',
    'fi',
    'fr',
    'gn',
    'he',
    'hr',
    'hu',
    'id',
    'is',
    'it',
    'ja',
    'kk',
    'km',
    'ko-KR',
    'kur-CKB',
    'lt',
    'lu',
    'lv',
    'ml',
    'mm',
    'ms',
    'my',
    'nb-NO',
    'nl',
    'pl',
    'pt',
    'pt-BR',
    'ro',
    'ru',
    'sk',
    'sl',
    'sm',
    'sr',
    'sr-CYR',
    'sv',
    'ta',
    'th',
    'tr',
    'ug',
    'uk',
    'uz-Cyrl',
    'uz-Latn',
    'vi',
    'zh-CN',
    'zh-TW',
}

#####################################################################################################

async def create_available_langs_list(app):
    translator_available_langs: Mapping[str, LanguageDetail] = await app.languages_service.get_lang_options()
    recognizer_available_langs: Mapping[str, LanguageDetail] = await app.rec_languages_service.get_recognizer_lang_options()
    app_available_langs = [lang.value for lang in LKey]
    intersected_codes = set(translator_available_langs.keys()).intersection(recognizer_available_langs.keys()).intersection(app_available_langs)
    available_langs = {}
    langs_directions = {}
    for l_code in intersected_codes:
        lang_name = translator_available_langs[l_code].code.split()[0].strip()
        available_langs[l_code] = lang_name
        langs_directions[l_code] = 'rtl' if translator_available_langs[l_code].rtl else 'ltr'

    sorted_available_langs = sorted(
        available_langs.items(),
        key=lambda unsorted_lang: TKey[f'T_{unsorted_lang[1].upper()}'](app.logger, LKey('ru')).lower(),
    )
    available_langs = {sort_lang: sort_code for sort_lang, sort_code in sorted_available_langs}
    return available_langs, langs_directions

#####################################################################################################

async def create_lang_list(app: App) -> dict[str, str]:
    _lang = app.app_settings.default_language_locale
    available_langs, _ = await create_available_langs_list(app)
    rus_available_langs = {}
    for code, en_lang_name in available_langs.items():
        tkey = TKey[f'T_{en_lang_name.upper()}']
        rus_name = tkey(app.logger, LKey(_lang)).strip().title()
        rus_available_langs[code] = rus_name
    return rus_available_langs

#####################################################################################################

def get_available_nicegui_lang(locale: str) -> Language:
    match locale:
        case "en":
            return "en-US"
        case "uz":
            return "uz-Cyrl"
        case "zh":
            return "zh-CN"
        case _:
            return locale if locale in _AVAILABLE_NICEGUI_LOCALES else 'en-US'

#####################################################################################################

def localize(phrase: TKey, locale: LKey = None, logger: Logger = None) -> str:
    if locale and logger:
        return phrase(logger=logger, locale=locale)

    if not isinstance(phrase, TKey):
        raise TypeError("'phrase' should be of")
    if not hasattr(nicegui_app, "app_settings") or not hasattr(nicegui_app, "logger"):
        raise AttributeError(
            f"{nicegui_app.__class__.__name__} instance has no required attributes. "
            f"'app_settings' and 'logger' attrs must be implemented."
        )
    default_lang = LKey(nicegui_app.app_settings.default_language_locale)
    logger = nicegui_app.logger

    return phrase(logger=logger, locale=default_lang)

#####################################################################################################

def _localize() -> Callable:
    validated_attrs = False
    default_lang = None
    logger = None

    def inner(phrase: TKey) -> str:
        nonlocal validated_attrs, default_lang, logger
        if not validated_attrs:
            if not isinstance(phrase, TKey):
                raise TypeError("'phrase' should be of TKey type")
            if not hasattr(nicegui_app, "app_settings") or not hasattr(nicegui_app, "logger"):
                raise AttributeError(
                    f"{nicegui_app.__class__.__name__} instance has no required attributes. "
                    f"'app_settings' and 'logger' attrs must be implemented."
                )
            default_lang = LKey(nicegui_app.app_settings.default_language_locale)
            logger = nicegui_app.logger
            validated_attrs = True
        return phrase(logger=logger, locale=default_lang)

    return inner

localize2 = _localize()
# usage: localize2(TKey.LOGIN)
