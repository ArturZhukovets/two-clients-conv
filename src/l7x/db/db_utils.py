#####################################################################################################

from datetime import datetime
from logging import Logger
from typing import Final, cast
from uuid import UUID

from argon2.exceptions import VerifyMismatchError
from databases import Database
from orjson import loads as orjson_loads
from ormar.queryset import FieldAccessor

from l7x.configs.constants import DEFAULT_ROOT_USER_LOGIN, DEFAULT_ROOT_USER_PASSWORD
from l7x.configs.settings import AppSettings
from l7x.db import DepartmentModel, UserModel
from l7x.db.base_meta import create_none_database, ormar_change_database
from l7x.utils.pwd_utils import create_password_hasher

#####################################################################################################

def get_db_url_from_app_settings(app_settings: AppSettings, use_db_admin_credentials: bool = False) -> str:
    db_user = app_settings.db_admin_user if use_db_admin_credentials else app_settings.db_user
    db_pass = app_settings.db_admin_pass if use_db_admin_credentials else app_settings.db_pass

    return (
        f'postgresql+asyncpg://{db_user}:{db_pass}@'
        + f'{app_settings.db_host}:{app_settings.db_port}/{app_settings.db_name}'
    )

#####################################################################################################

async def update_db_data(app_settings: AppSettings, logger: Logger) -> None:
    db_data_file: Final = app_settings.init_db_json_path

    if db_data_file is None:
        return

    if not db_data_file.exists():
        return

    logger.info(f'File {db_data_file.absolute()} with database data found. Starting data insertion process.')

    database: Final = Database(get_db_url_from_app_settings(app_settings, use_db_admin_credentials=True))
    ormar_change_database(database)

    try:
        await database.connect()
        with open(db_data_file, 'rb') as json_file:
            db_data = orjson_loads(json_file.read())
            departments = db_data.get('departments')
            users = db_data.get('users')

        async with database.transaction():
            if departments:
                for uuid, department in departments.items():
                    await DepartmentModel(primary_uuid=uuid, **department).upsert(__force_save__=True)
            if users:
                password_hasher = create_password_hasher(app_settings, logger)
                for uuid, user in users.items():
                    user['password'] = password_hasher.hash(user['password'])
                    await UserModel(primary_uuid=uuid, **user).upsert(__force_save__=True)
            logger.info('Data insertion process completed successfully.')
    except Exception as e:
        logger.error(f'Error occurred during data insertion process. Data not added to the database. Error: {e}')
    finally:
        ormar_change_database(create_none_database())
        await database.disconnect()

#####################################################################################################

def get_fa(model_field: str | int | bool | UUID | datetime | None) -> FieldAccessor:
    return cast(FieldAccessor, model_field)

#####################################################################################################

async def check_default_superuser(app_settings: AppSettings, logger: Logger) -> None:
    database: Final = Database(get_db_url_from_app_settings(app_settings, use_db_admin_credentials=True))
    ormar_change_database(database)
    password_hasher = create_password_hasher(app_settings, logger)
    try:
        await database.connect()
        user = await UserModel.objects.get_or_none(is_superuser=True, login=DEFAULT_ROOT_USER_LOGIN)
        if user is None:
            return
        user_pw_hash = user.password
        try:
            password_hasher.verify(user_pw_hash, DEFAULT_ROOT_USER_PASSWORD)
        except VerifyMismatchError:
            pass
        else:
            logger.warning('For security purposes, please change the default password of the default root user!')
    finally:
        ormar_change_database(create_none_database())
        await database.disconnect()

#####################################################################################################
