#####################################################################################################

import os
from asyncio import sleep
from dataclasses import dataclass
from functools import partial
from logging import Logger
from typing import Final, cast

from hypercorn.app_wrappers import ASGIWrapper
from hypercorn.asyncio.run import worker_serve
from hypercorn.config import Config as _HypercornConfig, Sockets
from hypercorn.logging import Logger as _HypercornLogger
from hypercorn.typing import AppWrapper, ASGIFramework
from nicegui.ui_run_with import run_with as _nicegui_run_with

from l7x.app import App
from l7x.commands.metrics_context_creator import MetricCmdManager
from l7x.configs.settings import AppSettings
from l7x.listeners import APP_LISTENERS_REGISTRARS
from l7x.utils.cmd_manager_utils import WorkerParams
from l7x.utils.lang_utils import get_available_nicegui_lang
from l7x.utils.loop_utils import CreateEventLoopParams, EventLoopFuncParams, ShutdownEvent, create_event_loop
from l7x.utils.worker_utils import StartedEvent

#####################################################################################################

@dataclass(frozen=True, kw_only=True)
class WebWorkerParams(WorkerParams):
    app_settings: AppSettings
    sockets: Sockets
    hypercorn_config: _HypercornConfig
    metrics_cmd_manager: MetricCmdManager | None = None

#####################################################################################################

@dataclass(frozen=True, kw_only=True)
class _ExtParams:
    loop_name: str
    sockets: Sockets
    hypercorn_config: _HypercornConfig
    metrics_cmd_manager: MetricCmdManager | None = None

#####################################################################################################

async def _check_multiprocess_shutdown_event(shutdown_event: ShutdownEvent, /) -> None:
    while True:
        if shutdown_event.is_set():
            return
        await sleep(0.1)

#####################################################################################################

async def _web_work(elp_params: EventLoopFuncParams[_ExtParams], /) -> None:
    logger: Final = elp_params.logger
    ext: Final = elp_params.ext
    logger.info(f'Worker process "{ext.loop_name}" starting...')

    app_settings: Final = elp_params.app_settings
    shutdown_event: Final = elp_params.shutdown_event

    shutdown_trigger = None
    if shutdown_event is not None:
        shutdown_trigger = partial(_check_multiprocess_shutdown_event, shutdown_event)

    app: Final = App(
        logger=logger,
        app_settings=app_settings,
        func_after_all_started=elp_params.func_after_all_started,
        metrics_cmd_manager=ext.metrics_cmd_manager,
    )

    for registrar in APP_LISTENERS_REGISTRARS:
        registrar(app)
    _language = get_available_nicegui_lang(locale=app_settings.default_language_locale)
    _nicegui_run_with(
        app,
        title=app_settings.web_app_title,
        language=_language,
        favicon='/static/images/favicon.ico',
        reconnect_timeout=10,
        storage_secret=app_settings.storage_secret,
        dark=False,
    )
    app_wrapper: Final = cast(AppWrapper, ASGIWrapper(cast(ASGIFramework, app)))

    class HypercornLoggerEx(_HypercornLogger):  # noqa: WPS431  # otherwise it is not possible to pass the logger inside
        def __init__(self, config: _HypercornConfig) -> None:
            super().__init__(config)
            self.access_logger = logger
            self.error_logger = logger
    ext.hypercorn_config.logger_class = HypercornLoggerEx
    ext.hypercorn_config.keep_alive_timeout = 60

    await worker_serve(app_wrapper, ext.hypercorn_config, sockets=ext.sockets, shutdown_trigger=shutdown_trigger)

#####################################################################################################

def run_web_worker(wp_params: WebWorkerParams, worker_name: str, shutdown_event: ShutdownEvent, started_event: StartedEvent, /) -> None:
    app_settings: Final = wp_params.app_settings
    sockets: Final = wp_params.sockets
    metrics_cmd_manager: Final = wp_params.metrics_cmd_manager
    hypercorn_config: Final = wp_params.hypercorn_config

    def after_all_started(logger: Logger) -> None:
        logger.info(f'Worker process "{worker_name}" started')
        started_event.set()

    create_event_loop(CreateEventLoopParams(
        func=_web_work,
        app_settings=app_settings,
        loop_name=worker_name,
        shutdown_event=shutdown_event,
        ext=_ExtParams(
            loop_name=worker_name,
            sockets=sockets,
            hypercorn_config=hypercorn_config,
            metrics_cmd_manager=metrics_cmd_manager,
        ),
        func_after_all_started=after_all_started,
    ))

#####################################################################################################
