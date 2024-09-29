#####################################################################################################

from contextlib import asynccontextmanager
from functools import partial
from logging import Logger
from typing import Final

from databases import Database
from nicegui.core import app as _nicegui_app

from l7x.commands.metrics_context_creator import MetricCmdManager
from l7x.configs.settings import AppSettings
from l7x.db import ConversationModel
from l7x.db.base_meta import ormar_change_database
from l7x.db.db_utils import get_db_url_from_app_settings
from l7x.middleware import AdminMiddleware, AuthMiddleware
from l7x.services.langs_service import PrivateLangsService
from l7x.services.recognize_langs_service import PrivateRecognizerLangsService
from l7x.services.recognize_service import PrivateRecognizeService
from l7x.services.translation_service import PrivateTranslationService
from l7x.utils.aiohttp_utils import create_aiohttp_client

from l7x.utils.fastapi_utils import AppFastAPI
from l7x.utils.loop_utils import AfterAllStartedFunc
from l7x.utils.storage_utils import ConversationStorageHelper


#####################################################################################################

class App(AppFastAPI):
    #####################################################################################################

    def __init__(
        self,
        logger: Logger,
        app_settings: AppSettings,
        func_after_all_started: AfterAllStartedFunc | None = None,
        metrics_cmd_manager: MetricCmdManager | None = None,
    ) -> None:
        def on_startup() -> None:
            if func_after_all_started is not None:
                func_after_all_started(logger)

        async def close_conv_on_startup(db: Database):
            try:
                d = True
                async with db:
                    await ConversationModel.close_all_unclosed()
                print("ALL CONVERSATIONS WERE CLOSED")
            finally:
                d = False
                # await db.disconnect()

        super().__init__(logger, app_settings, on_startup=[on_startup])

        self._database: Final = Database(get_db_url_from_app_settings(app_settings, use_db_admin_credentials=True))
        ormar_change_database(self._database)
        self.upgrade_lifespan()

        self._aiohttp_client: Final = create_aiohttp_client()

        _nicegui_app.password_hasher = self._password_hasher
        _nicegui_app.logger = self.logger
        _nicegui_app.database = self._database
        _nicegui_app.languages_service = PrivateLangsService(app_settings, self._aiohttp_client, logger)
        _nicegui_app.translation_service = PrivateTranslationService(app_settings, self._aiohttp_client, logger)
        _nicegui_app.recognize_service = PrivateRecognizeService(app_settings, self._aiohttp_client, logger)
        _nicegui_app.rec_languages_service = PrivateRecognizerLangsService(app_settings, self._aiohttp_client, logger)
        _nicegui_app.add_static_files(url_path='/static', local_directory='./static')
        _nicegui_app.app_settings = app_settings
        _nicegui_app.metrics_cmd_manager = metrics_cmd_manager
        _nicegui_app.conversations_storage = ConversationStorageHelper(_nicegui_app)
        # _nicegui_app.on_startup(partial(close_conv_on_startup, self._database))

        _nicegui_app.add_middleware(AdminMiddleware)
        _nicegui_app.add_middleware(AuthMiddleware)

    def upgrade_lifespan(self):
        original_lifespan_context = self.router.lifespan_context

        @asynccontextmanager
        async def lifespan_wrapper(app):
            await self._database.connect()
            await ConversationModel.close_all_unclosed()
            async with original_lifespan_context(app):
                yield
            await self._database.disconnect()

        self.router.lifespan_context = lifespan_wrapper

#####################################################################################################
