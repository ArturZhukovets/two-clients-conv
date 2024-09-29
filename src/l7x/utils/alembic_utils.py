#####################################################################################################

from collections.abc import Iterator
from typing import Final

from alembic.config import Config
from alembic.runtime.environment import EnvironmentContext
from alembic.runtime.migration import RevisionStep
from alembic.script import Script, ScriptDirectory
from alembic.script.revision import RevisionMap

from l7x.alembic.migrations import MIGRATIONS
from l7x.configs.settings import AppSettings
from l7x.db.db_utils import get_db_url_from_app_settings

#####################################################################################################

class _ScriptDirectory(ScriptDirectory):
    #####################################################################################################

    def __init__(self, config: Config) -> None:  # pylint: disable=super-init-not-called
        self.dir = ''
        self.file_template = ''
        self.version_locations = None
        self.truncate_slug_length = 40
        self.sourceless = True
        self.output_encoding = config.get_main_option('output_encoding', 'utf-8')
        self.revision_map = RevisionMap(self._load_revisions)
        self.timezone = config.get_main_option('timezone')
        self.hook_config = config.get_section('post_write_hooks', {})

    #####################################################################################################

    def _load_revisions(self) -> Iterator[Script]:
        yield from (
            Script(migration, migration.revision, '') for migration in MIGRATIONS
        )

#####################################################################################################

def upgrade_db_to_head(app_settings: AppSettings) -> None:
    config: Final = Config()
    config.set_main_option('sqlalchemy.url', get_db_url_from_app_settings(app_settings, use_db_admin_credentials=True))
    config.set_main_option('output_encoding', 'utf-8')
    config.set_main_option('timezone', 'UTC')

    script = _ScriptDirectory(config)

    revision: Final = 'head'

    def upgrade(rev: str, _context: EnvironmentContext) -> list[RevisionStep]:
        return script._upgrade_revs(revision, rev)  # noqa: WPS437 # pylint: disable=protected-access

    with EnvironmentContext(
        config,
        script,
        fn=upgrade,
        as_sql=False,
        starting_rev=None,
        destination_rev=revision,
        tag=None,
    ):
        from l7x.alembic.db_migrations import run_db_migrations  # noqa: WPS433 # pylint: disable=import-outside-toplevel

        run_db_migrations()

#####################################################################################################
