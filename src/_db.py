#!/usr/bin/env -S poetry run python

#####################################################################################################
"""
Alembic wrapper. Utility to manage database.

Usage:
    ./src/_db.py -h
    ./src/_db.py revision --autogenerate -m "Revision name"
    ./src/_db.py upgrade head
    ./src/_db.py downgrade -1
"""
#####################################################################################################

# pylint: disable=wrong-import-position, wrong-import-order
from typing import Final

from l7x.logger import setup_logging  # !!! MUST BE FIRST IMPORT !!!

# pylint: enable=wrong-import-position

_LOGGER: Final = setup_logging(default_path='logging_debug.json')

#####################################################################################################

from argparse import ArgumentDefaultsHelpFormatter, Namespace  # noqa: E402
from logging import Logger  # noqa: E402
from os.path import isabs as _path_isabs, join as _path_join  # noqa: E402
from pathlib import Path  # noqa: E402
from sys import exit as _sys_exit  # noqa: E402

from alembic.config import CommandLine, Config  # noqa: E402

from l7x.configs.settings import create_app_settings  # noqa: E402
from l7x.db.db_utils import get_db_url_from_app_settings  # noqa: E402

#####################################################################################################

_PROJECT_PATH: Final = Path(__file__).parent.parent.resolve()

#####################################################################################################

def _make_alembic_config(cmd_opts: Namespace, base_path: Path = _PROJECT_PATH) -> Config:
    # Replace path to alembic.ini file to absolute
    if not _path_isabs(cmd_opts.config):
        cmd_opts.config = _path_join(base_path, cmd_opts.config)

    config: Final = Config(file_=cmd_opts.config, ini_section=cmd_opts.name, cmd_opts=cmd_opts)

    # Replace path to alembic folder to absolute
    alembic_location: Final = config.get_main_option('script_location')
    if alembic_location is not None and not _path_isabs(alembic_location):
        config.set_main_option('script_location', _path_join(base_path, alembic_location))

    if cmd_opts.pg_url:
        config.set_main_option('sqlalchemy.url', cmd_opts.pg_url)

    return config

#####################################################################################################

def _main(logger: Logger) -> None:
    logger.debug('DB wrapper utility...')
    app_settings: Final = create_app_settings(include_db_admin_credentials=True)

    alembic: Final = CommandLine()
    alembic.parser.formatter_class = ArgumentDefaultsHelpFormatter
    alembic.parser.add_argument(
        '--pg-url',
        default=get_db_url_from_app_settings(app_settings, use_db_admin_credentials=True),
        help='PostgreSQL URL',
    )

    exit_code = 1
    options = alembic.parser.parse_args()
    if 'cmd' not in options:
        alembic.parser.error('too few arguments')
    else:
        config: Final = _make_alembic_config(options)
        alembic.run_cmd(config, options)
        exit_code = 0

    _sys_exit(exit_code)

#####################################################################################################

if __name__ == '__main__':
    _main(_LOGGER)

#####################################################################################################
