from dataclasses import dataclass
from datetime import datetime
from logging import Logger, getLogger
from time import monotonic, sleep
from typing import Final

from databases import Database

from l7x.configs.settings import AppSettings
from l7x.db import SessionModel
from l7x.db.base_meta import ormar_change_database
from l7x.db.db_utils import get_db_url_from_app_settings
from l7x.logger import DEFAULT_LOGGER_NAME
from l7x.types.errors import AppException, ShutdownException
from l7x.types.shutdown_event import ShutdownEvent
from l7x.utils.apm_utils import init_apm_client, init_elastic_log
from l7x.utils.cmd_manager_utils import WorkerParams
from l7x.utils.datetime_utils import now_utc, offset_time
from l7x.utils.loop_utils import EventLoopContext, _create_event_loop, _finalize_event_loop
from l7x.utils.worker_utils import StartedEvent

#####################################################################################################

@dataclass(frozen=True, kw_only=True)
class SessionWorkerParams(WorkerParams):
    app_settings: AppSettings

#####################################################################################################

async def check_sessions(logger: Logger):
    open_sessions = await SessionModel.objects \
        .select_related('user_id__department_id') \
        .prefetch_related('conversations') \
        .filter(logout_ts__isnull=True).all()
    if open_sessions:
        for session in open_sessions:
            timezone = session.user_id.department_id.timezone
            current_utc_ts = datetime.utcnow()
            login_ts = offset_time(session.login_ts, timezone)
            current_ts = offset_time(current_utc_ts, timezone)

            session_uuid = session.primary_uuid

            if login_ts.date() != current_ts.date():
                session = await session.upsert(logout_ts=now_utc())
                for conversation in session.conversations:
                    if conversation.end_ts is None:
                        await conversation.upsert(end_ts=now_utc())
                        logger.info(f'Conversation {session_uuid} has been closed.')

                logger.info(f'Session {session_uuid} has been closed.')

#####################################################################################################

async def _run_sessions_check(
    *,
    app_settings: AppSettings,
    shutdown_event: ShutdownEvent,
    loop_name: str,
    logger: Logger,
    apm_client,
    func_after_all_started,
) -> None:
    if loop_name != '':
        logger.info(f'Worker process "{loop_name}" starting...')
    database: Final = Database(get_db_url_from_app_settings(app_settings, use_db_admin_credentials=True))
    ormar_change_database(database)

    await database.connect()

    delay_sec: Final = app_settings.check_sessions_interval_sec

    func_after_all_started(logger)

    preview_time_check: float = -1.0

    while not shutdown_event.is_set():
        cur_time = monotonic()
        if preview_time_check > 0 and preview_time_check + delay_sec > cur_time:
            sleep(1)
            continue
        try:
            await check_sessions(logger)
            preview_time_check = cur_time
        except BaseException as err:  # noqa: WPS424
            if not isinstance(err, ShutdownException):
                logger.error(f'session_check: {err}', exc_info=err)
            if apm_client is not None:
                apm_client.capture_exception(err)  # type: ignore[no-untyped-call]
            if not isinstance(err, ShutdownException):
                raise ShutdownException() from err
            raise err

    await database.disconnect()

#####################################################################################################

def run_session_check_worker(wp_params: SessionWorkerParams, worker_name: str | None, shutdown_event: ShutdownEvent, started_event: StartedEvent, /) -> None:
    app_settings: Final = wp_params.app_settings
    logger: Final = getLogger(DEFAULT_LOGGER_NAME if worker_name == '' else worker_name)
    init_elastic_log(app_settings)
    apm_client: Final = init_apm_client(logger, app_settings)

    def after_all_started(logger: Logger) -> None:
        logger.info(f'Worker process "{worker_name}" started')
        started_event.set()

    loop: Final = _create_event_loop(app_settings.is_dev_mode)

    try:
        context = loop.run_until_complete(_run_sessions_check(
            loop_name=worker_name,
            app_settings=app_settings,
            logger=logger,
            apm_client=apm_client,
            shutdown_event=shutdown_event,
            func_after_all_started=after_all_started,
        ))

        if context is not None:
            if not isinstance(context, EventLoopContext):
                raise AppException('Loop context unknown class')

            if context.wait_set_shutdown_event and not shutdown_event.is_set():
                shutdown_event_wait_obj = loop.run_in_executor(None, shutdown_event.wait)
                loop.run_until_complete(shutdown_event_wait_obj)

    except (KeyboardInterrupt, ShutdownException) as err:
        logger.info('Shutdown...')
        shutdown_event.set()
        if isinstance(err, ShutdownException):
            raise err
        raise ShutdownException() from err

    except BaseException as err:  # noqa: WPS424 # pylint: disable=broad-except
        if apm_client is not None:
            apm_client.capture_exception()  # type: ignore[no-untyped-call]
        logger.error(f'Create loop error: {err}', exc_info=err)
        raise err
    finally:
        _finalize_event_loop(loop, logger, apm_client)

#####################################################################################################
