#####################################################################################################
from collections.abc import Iterable, Mapping, Sequence

from l7x.types.lang_services import LanguageDetail

#####################################################################################################

def is_valid_language(lang: str, available_langs: Mapping[str, LanguageDetail]) -> bool:
    return lang in available_langs

#####################################################################################################

def filter_only_valid_languages(langs_for_filter: Iterable[str], available_langs: Mapping[str, LanguageDetail]) -> Sequence[str]:
    ret: list[str] = []
    for lang in langs_for_filter:
        if is_valid_language(lang, available_langs):
            ret.append(lang)
    return tuple(ret)

#####################################################################################################

def check_language(lang: str, available_langs: Mapping[str, LanguageDetail]) -> str:
    lang = lang.strip()
    return lang if is_valid_language(lang, available_langs) else ''

#####################################################################################################
