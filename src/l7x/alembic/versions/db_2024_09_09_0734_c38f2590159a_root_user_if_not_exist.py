#####################################################################################################
"""root_user_if_not_exist

Revision ID: c38f2590159a
Revises: a94c970ba137
Create Date: 2024-09-09 07:34:56.616005+00:00

"""
#####################################################################################################

from collections.abc import Sequence
from logging import getLogger
from typing import Final

import sqlalchemy as sa
from alembic import op

from l7x.configs.settings import create_app_settings
from l7x.logger import DEFAULT_LOGGER_NAME
from l7x.utils.pwd_utils import create_password_hasher
from l7x.configs.constants import DEFAULT_ROOT_USER_LOGIN, DEFAULT_ROOT_USER_PASSWORD

#####################################################################################################

# revision identifiers, used by Alembic.
# pylint: disable=invalid-name
revision: Final[str] = 'c38f2590159a'
down_revision: Final[str | None] = 'a94c970ba137'
branch_labels: Final[Sequence[str] | None] = None
depends_on: Final[str | None] = None
_DEFAULT_DEPARTMENT_UUID: Final[str] = '00000000-0000-0000-0000-000000000000'
# pylint: enable=invalid-name

#####################################################################################################

def upgrade() -> None:
    connection = op.get_bind()
    user = connection.execute(
        sa.text("SELECT 1 FROM users WHERE is_superuser = true LIMIT 1")
    ).fetchone()
    if user:
        return
    department = connection.execute(
        sa.text(
            """
            SELECT primary_uuid
            FROM departments
            WHERE primary_uuid = :primary_uuid;
            """
        ).bindparams(primary_uuid=_DEFAULT_DEPARTMENT_UUID)
    ).fetchone()
    if not department:
        department_name = "default"
        department_address = "1st April, Athienou"
        department_timezone = "+00:00"
        connection.execute(
            sa.text(
                """
                INSERT INTO departments (primary_uuid, name, address, timezone)
                VALUES (:primary_uuid, :name, :address, :timezone);
                """
            ).bindparams(
                primary_uuid=_DEFAULT_DEPARTMENT_UUID,
                name=department_name,
                address=department_address,
                timezone=department_timezone,
            )
        )

    app_settings = create_app_settings()
    hasher = create_password_hasher(app_settings, logger=getLogger(DEFAULT_LOGGER_NAME))
    hashed_pwd: Final = hasher.hash(password=DEFAULT_ROOT_USER_PASSWORD)

    connection.execute(
        sa.text(
            """
            INSERT INTO users (login, full_name, password, is_active, is_superuser, department_id)
            VALUES (:login, :full_name, :password, :is_active, :is_superuser, :department_id);
            """
        ).bindparams(
            login=DEFAULT_ROOT_USER_LOGIN,
            full_name='Default Root User',
            password=hashed_pwd,
            is_active=True,
            is_superuser=True,
            department_id=_DEFAULT_DEPARTMENT_UUID,
        )
    )
    return

#####################################################################################################

def downgrade() -> None:
    connection = op.get_bind()
    user = connection.execute(
        sa.text("SELECT 1 FROM users WHERE login = :login LIMIT 1").bindparams(login=DEFAULT_ROOT_USER_LOGIN)
    ).fetchone()
    if user:
        # TODO Если ошибка из-за привязанных к пользователю sessions / conversations то пофиксить это место
        connection.execute(
            sa.text(
                """
                DELETE FROM users
                WHERE login = :login;
                """
            ).bindparams(login=DEFAULT_ROOT_USER_LOGIN)
        )

    # Check if there are users connected to default department
    users_count = connection.execute(
        sa.text(
            """
            SELECT COUNT(*) FROM users
            WHERE department_id = :department_id
            """
        ).bindparams(department_id=_DEFAULT_DEPARTMENT_UUID)
    ).fetchone().count
    if users_count > 0:
        getLogger(DEFAULT_LOGGER_NAME).warning(
            'it is impossible to delete default department because there are users linked to them'
        )
        return
    connection.execute(
        sa.text(
            """
            DELETE FROM departments
            WHERE primary_uuid = :primary_uuid
            """
        ).bindparams(primary_uuid=_DEFAULT_DEPARTMENT_UUID)
    )

#####################################################################################################
