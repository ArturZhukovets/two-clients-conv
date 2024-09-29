#####################################################################################################

from datetime import datetime, timedelta, timezone, tzinfo
from re import Pattern, compile
from typing import Any, Final, AnyStr

#####################################################################################################

TIME_OFFSET_VALIDATION_PATTERN: Pattern[str] = compile(r'^[+-]\d{2}:\d{2}$')

#####################################################################################################

class _Utc(tzinfo):
    #####################################################################################################

    _ZERO: Final = timedelta(0)

    __slots__ = ()

    #####################################################################################################

    def utcoffset(self, _: datetime | None) -> timedelta:
        return self._ZERO

    #####################################################################################################

    def dst(self, _: datetime | None) -> timedelta:
        return self._ZERO

    #####################################################################################################

    def tzname(self, _: datetime | None) -> str:
        return 'UTC'

#####################################################################################################

def _get_utc() -> tzinfo:
    try:
        utc: tzinfo | None = timezone.utc
    except AttributeError:
        utc = None

    if utc is None:
        return _Utc()
    return utc

#####################################################################################################

UTC_ZONE: Final = _get_utc()

#####################################################################################################

def now_utc() -> datetime:
    return replace_datetime_timezone_to_utc(datetime.now(UTC_ZONE))

#####################################################################################################

def zero_utc() -> datetime:
    return replace_datetime_timezone_to_utc(datetime.fromtimestamp(0, UTC_ZONE))

#####################################################################################################

def replace_datetime_timezone_to_utc_none(datetime_for_replace: datetime | None) -> datetime | None:
    return replace_datetime_timezone_to_utc(datetime_for_replace) if datetime_for_replace is not None else None

#####################################################################################################

def replace_datetime_timezone_to_utc(datetime_for_replace: datetime) -> datetime:
    return datetime_for_replace.replace(tzinfo=UTC_ZONE) if datetime_for_replace.tzinfo is None else datetime_for_replace

#####################################################################################################

def replace_datetime_timezone_to_utc_in_dict(dict_with_dt: dict[str, Any], *field_names: str) -> None:
    for field_name in field_names:
        datetime_for_replace = dict_with_dt.get(field_name)
        if datetime_for_replace is None:
            continue
        if not isinstance(datetime_for_replace, datetime):
            raise ValueError(f'{field_name} is not datetime')
        dict_with_dt[field_name] = replace_datetime_timezone_to_utc_none(datetime_for_replace)

#####################################################################################################

def offset_time(dt: datetime, offset: str) -> datetime:
    sign = 1 if offset[0] == '+' else -1
    hours, minutes = map(int, offset[1:].split(':'))
    return dt + timedelta(hours=sign * hours, minutes=sign * minutes)

#####################################################################################################

def generate_midnight_datetime(offset: str | None = None) -> datetime:
    if offset is None:
        dt = datetime.utcnow()
    else:
        dt = offset_time(datetime.utcnow(), offset)
    return dt.replace(hour=23, minute=59, second=0, microsecond=0)

#####################################################################################################

def format_datetime_to_iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

#####################################################################################################

def validate_time_offset(offset: str) -> bool:
    if TIME_OFFSET_VALIDATION_PATTERN.match(offset):
        return True
    else:
        return False

#####################################################################################################

def timedelta_to_str(timedelta: timedelta) -> str:
    hours, remainder = divmod(timedelta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f'{hours:02}:{minutes:02}:{seconds:02}'

#####################################################################################################

def datetime_to_q_date(dt: datetime, separator: str = '-') -> str:
    return dt.strftime(f'%d{separator}%m{separator}%Y')

#####################################################################################################

def datetime_to_q_date_props(dt: datetime, separator: str = '/') -> str:
    return dt.strftime(f'%Y{separator}%m{separator}%d')

#####################################################################################################

def q_date_to_utc_datetime(date_str: str, mask: str = '%d-%m-%Y') -> datetime:
    return datetime.strptime(date_str, mask).replace(tzinfo=timezone.utc)

#####################################################################################################

def validate_q_date(q_date: str) -> bool:
    try:
        q_date_to_utc_datetime(q_date)
        return True
    except BaseException:
        return False

#####################################################################################################
