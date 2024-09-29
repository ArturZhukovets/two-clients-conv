#####################################################################################################

from collections.abc import Mapping
from logging import Logger
from multiprocessing import cpu_count
from os import environ, getenv
from pathlib import Path
from sys import flags
from typing import Any, Final, Protocol, TypeVar
from urllib.parse import urlparse

from environs import Env
from pydantic.dataclasses import dataclass

from l7x.types.language import LKey
from l7x.utils.config_utils import get_app_build_info
from l7x.utils.orjson_utils import orjson_dumps_to_str_pretty

#####################################################################################################

def load_env() -> Env:
    env: Final = Env()

    env_file: Final = './.env'
    if Path(env_file).exists():
        env.read_env(env_file, override=True)

    return env

#####################################################################################################

def _resolve_path(path: str) -> Path | None:
    return Path(path).resolve() if path != '' else None

#####################################################################################################

_AppSettingsExt = TypeVar('_AppSettingsExt', bound='AppSettings')

@dataclass(frozen=True, kw_only=True)
class AppSettings:  # pylint: disable=too-many-instance-attributes
    #####################################################################################################

    service_name: str
    service_version: str
    service_branch: str
    service_commit_hash: str
    service_build_timestamp: str

    is_dev_mode: bool

    port: int
    worker_count: int
    server_url: str

    # TODO: вынести логику с apm в паблик-бот
    is_elastic_apm_server_enabled: bool
    elastic_apm_server_url: str

    is_send_to_elastic_log_server: bool
    elastic_log_server_host: str
    elastic_log_server_port: int
    elastic_log_server_user: str
    elastic_log_server_pass: str

    localtunnel_user: str
    localtunnel_pass: str

    db_pass: str
    db_name: str
    db_user: str
    db_host: str
    db_port: int
    # db_secret: bytes

    db_admin_user: str
    db_admin_pass: str

    translate_api_url: str
    translate_api_langs_cache_expire_sec: int

    max_upload_file_size_in_byte: int

    check_sessions_interval_sec: int
    init_db_json_path: Path | None

    storage_secret: str

    certificate_path: Path | None
    private_key_path: Path | None

    pwd_salt_len: int
    pwd_hash_len: int
    pwd_time_cost: int
    pwd_memory_cost_kib: int
    pwd_parallelism: int

    compute_metrics_device: str
    compute_metrics_timeout_sec: int
    metrics_cache_path: Path | None

    default_language_locale: str

    enable_admin_pages: bool

    web_app_title: str

    enable_questionnaire: bool
    enable_base_lang_select: bool

    #####################################################################################################

    def __str__(self, /) -> str:
        obj_for_output: Final = self._get_fields_for_output()
        return orjson_dumps_to_str_pretty(obj_for_output)

    #####################################################################################################

    def _get_fields_for_output(self) -> Mapping[str, Any]:
        obj_for_output = {
            'SERVICE_NAME': self.service_name,
            'SERVICE_VERSION': self.service_version,

            'SERVER_PORT': self.port,
            'WORKER_COUNT': self.worker_count,
            'SERVER_EXTERNAL_URL': self.server_url,

            'DB_NAME': self.db_name,
            'DB_USER': self.db_user,
            'DB_HOST': self.db_host,
            'DB_PORT': self.db_port,

            'TRANSLATE_API_URL': self.translate_api_url,
            'TRANSLATE_API_LANGS_CACHE_EXPIRE_SEC': self.translate_api_langs_cache_expire_sec,

            'MAX_UPLOAD_FILE_SIZE_IN_BYTE': self.max_upload_file_size_in_byte,

            'COMPUTE_METRICS_DEVICE': self.compute_metrics_device,
            'COMPUTE_METRICS_TIMEOUT_SEC': self.compute_metrics_timeout_sec,
            'METRICS_CACHE_PATH': self.metrics_cache_path,

            'WEB_APP_TITLE': self.web_app_title,
            'ENABLE_QUESTIONNAIRE': self.enable_questionnaire,
            'ENABLE_BASE_LANG_SELECT': self.enable_questionnaire,
        }

        if self.is_dev_mode:
            obj_for_output.update({
                '_IS_DEV_MODE_': self.is_dev_mode,

                'SERVICE_BRANCH': self.service_branch,
                'SERVICE_COMMIT_HASH': self.service_commit_hash,
                'SERVICE_BUILD_TIMESTAMP': self.service_build_timestamp,

                'ELASTIC_APM_SERVER_ENABLED': self.is_elastic_apm_server_enabled,
                'ELASTIC_APM_SERVER_URL': self.elastic_apm_server_url,

                'IS_SEND_TO_ELASTIC_LOG_SERVER': self.is_send_to_elastic_log_server,
                'ELASTIC_LOG_SERVER_HOST': self.elastic_log_server_host,
                'ELASTIC_LOG_SERVER_PORT': self.elastic_log_server_port,
                'ELASTIC_LOG_SERVER_USER': self.elastic_log_server_user,
                'ELASTIC_LOG_SERVER_PASS': self.elastic_log_server_pass,

                'LOCALTUNNEL_USER': self.localtunnel_user,
                'LOCALTUNNEL_PASS': self.localtunnel_pass,

                'DB_PASS': self.db_pass,

                'DB_ADMIN_USER': self.db_admin_user,
                'DB_ADMIN_PASS': self.db_admin_pass,

                # 'DB_SECRET': self.db_secret.hex(),

                'PWD_SALT_LEN': self.pwd_salt_len,
                'PWD_HASH_LEN': self.pwd_hash_len,
                'PWD_TIME_COST': self.pwd_time_cost,
                'PWD_MEMORY_COST_KIB': self.pwd_memory_cost_kib,
                'PWD_PARALLELISM': self.pwd_parallelism,

                'ENABLE_ADMIN_PAGES': self.enable_admin_pages,
            })
        return obj_for_output

    #####################################################################################################

    def cast(self, app_settings_class: type[_AppSettingsExt]) -> _AppSettingsExt:
        if not isinstance(self, app_settings_class):
            raise TypeError(f'Settings cant cast to "{app_settings_class}"')
        return self

#####################################################################################################

class _AppSettingsProtocol(Protocol):
    def __call__(self, include_db_admin_credentials: bool = False, logger: Logger | None = None) -> AppSettings:
        raise NotImplementedError()

#####################################################################################################

def _create_app_settings() -> _AppSettingsProtocol:
    dev_translate_api_url = None

    def _app_settings(include_db_admin_credentials: bool = False, *, logger: Logger | None = None) -> AppSettings:
        translate_api_url = urlparse(getenv('L7X_TRANSLATE_API_URL', '')).geturl()

        nonlocal dev_translate_api_url  # noqa: WPS420
        if dev_translate_api_url is None:
            dev_translate_api_url = translate_api_url  # noqa: WPS442

        env: Final = load_env()

        run_translation_server: Final = env.bool('L7X_RUN_TRANSLATION_SERVER', False)  # noqa: WPS425
        is_dev_mode: Final = flags.dev_mode is True

        if is_dev_mode and run_translation_server:
            translate_api_url = dev_translate_api_url
        else:
            translate_api_url = urlparse(env.str('L7X_TRANSLATE_API_URL', '')).geturl()

        metrics_cache_path: Final = _resolve_path(env.str('L7X_METRICS_CACHE_PATH', ''))
        if metrics_cache_path is not None:
            environ['FAIRSEQ2_CACHE_DIR'] = str(metrics_cache_path)  # for SONAR metric models
            environ['HF_HOME'] = str(metrics_cache_path)  # for COMET metric models

        app_build_info: Final = get_app_build_info()

        db_admin_pass = ''
        db_admin_user = ''
        if include_db_admin_credentials:
            db_admin_pass = env.str('L7X_DB_ADMIN_PASS', '').strip()
            db_admin_user = env.str('L7X_DB_ADMIN_USER', 'demo_page').strip()

        _default_lang_locale = env.str('L7X_DEFAULT_LANGUAGE_LOCALE', 'en')
        if _default_lang_locale not in set(e.value for e in LKey):
            if logger is not None:
                logger.warning(
                    f'The value of L7X_DEFAULT_LANGUAGE_LOCALE={_default_lang_locale}'
                    ' does not match any of the available locales.\n'
                    'The application will be launched in English.'
                )
            _default_lang_locale = 'en'

        return AppSettings(
            service_name=env.str('L7X_SERVICE_NAME', app_build_info.app_name).strip(),
            service_version=app_build_info.app_version,
            service_branch=app_build_info.app_branch,
            service_commit_hash=app_build_info.app_commit_hash,
            service_build_timestamp=app_build_info.app_build_timestamp,

            is_dev_mode=is_dev_mode,

            port=env.int('L7X_SERVER_PORT', 8080),  # noqa: WPS432
            worker_count=env.int('L7X_WORKER_COUNT', (cpu_count() * 2) + 1),
            server_url=urlparse(env.str('L7X_SERVER_EXTERNAL_URL')).geturl(),

            is_elastic_apm_server_enabled=env.bool('L7X_ELASTIC_APM_SERVER_ENABLED', False),  # noqa: WPS425
            elastic_apm_server_url=urlparse(env.str('L7X_ELASTIC_APM_SERVER_URL', '')).geturl(),

            is_send_to_elastic_log_server=env.bool('L7X_IS_SEND_TO_ELASTIC_LOG_SERVER', False),  # noqa: WPS425
            elastic_log_server_host=urlparse(env.str('L7X_ELASTIC_LOG_SERVER_HOST', '')).geturl(),
            elastic_log_server_port=env.int('L7X_ELASTIC_LOG_SERVER_PORT', 9200),  # noqa: WPS432
            elastic_log_server_user=env.str('L7X_ELASTIC_LOG_SERVER_USER', 'elastic').strip(),
            elastic_log_server_pass=env.str('L7X_ELASTIC_LOG_SERVER_PASS', 'changeme').strip(),

            localtunnel_user=env.str('L7X_LOCALTUNNEL_USER', '').strip(),
            localtunnel_pass=env.str('L7X_LOCALTUNNEL_PASS', '').strip(),

            db_pass=env.str('L7X_DB_PASS', '').strip(),
            db_name=env.str('L7X_DB_NAME', 'demo_page').strip(),
            db_user=env.str('L7X_DB_USER', 'demo_page').strip(),
            db_host=env.str('L7X_DB_HOST', 'localhost').strip(),
            db_port=env.int('L7X_DB_PORT', 5432),  # noqa: WPS432
            # db_secret=calc_secrets(env.str('L7X_DB_SECRET', '').strip()),

            db_admin_pass=db_admin_pass,
            db_admin_user=db_admin_user,

            translate_api_url=translate_api_url,
            translate_api_langs_cache_expire_sec=env.int('L7X_TRANSLATE_API_LANGS_CACHE_EXPIRE_SEC', 60 * 60),

            max_upload_file_size_in_byte=env.int('L7X_MAX_UPLOAD_FILE_SIZE_IN_BYTE', 50 * 1024 * 1024),  # noqa: WPS432

            check_sessions_interval_sec=env.int('L7X_CHECK_SESSIONS_INTERVAL_SEC', 60),
            init_db_json_path=None,  # _resolve_path(env.str('L7X_INIT_DB_JSON_PATH', '')),

            storage_secret=env.str('L7X_STORAGE_SECRET', ''),

            certificate_path=_resolve_path(env.str('L7X_SSL_CERTIFICATE_PATH', '')),
            private_key_path=_resolve_path(env.str('L7X_SSL_PRIVATE_KEY_PATH', '')),

            pwd_salt_len=env.int('L7X_PWD_SALT_LEN', 16),
            pwd_hash_len=env.int('L7X_PWD_HASH_LEN', 32),
            pwd_time_cost=env.int('L7X_PWD_TIME_COST', 16),
            pwd_memory_cost_kib=env.int('L7X_MEMORY_COST_KIB', 2097152),
            pwd_parallelism=env.int('L7X_PWD_PARALLELISM', 8),

            compute_metrics_device=env.str('L7X_COMPUTE_METRICS_DEVICE', 'cpu'),
            compute_metrics_timeout_sec=env.int('L7X_COMPUTE_METRICS_TIMEOUT_SEC', 120),
            metrics_cache_path=metrics_cache_path,

            default_language_locale=_default_lang_locale,

            enable_admin_pages=env.bool('L7X_ENABLE_ADMIN_PAGES', False),  # noqa: WPS425

            web_app_title=env.str('L7X_WEB_APP_TITLE', app_build_info.app_name).strip(),

            enable_questionnaire=env.bool('L7X_ENABLE_QUESTIONNAIRE', True),
            enable_base_lang_select=env.bool('L7X_ENABLE_BASE_LANG_SELECT', False),
        )

    return _app_settings

#####################################################################################################

create_app_settings = _create_app_settings()

#####################################################################################################
