#####################################################################################################
"""Init DB.

Revision ID: dcbcd14d03c3
Revises:
Create Date: 2024-05-16 13:04:01.495517+00:00

"""
#####################################################################################################

from collections.abc import Sequence
from typing import Final

from alembic.op import create_table, drop_table, f as _alembic_f
from sqlalchemy import JSON, Boolean, Column, ForeignKeyConstraint, LargeBinary, PrimaryKeyConstraint, String, Text, UniqueConstraint, text

from l7x.db.db_types import POSTGRESQL_DATETIME, POSTGRESQL_UUID

#####################################################################################################

# revision identifiers, used by Alembic.
# pylint: disable=invalid-name
revision: Final[str] = 'dcbcd14d03c3'
down_revision: Final[str | None] = None
branch_labels: Final[Sequence[str] | None] = None
depends_on: Final[str | None] = None
# pylint: enable=invalid-name

#####################################################################################################

def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    create_table(
        'departments',
        Column('primary_uuid', POSTGRESQL_UUID, server_default=text('gen_random_uuid()'), nullable=False),
        Column('name', String(length=1000), nullable=True),
        Column('address', String(length=1000), nullable=True),
        Column('timezone', String(length=200), nullable=False),
        PrimaryKeyConstraint('primary_uuid', name=_alembic_f('pk__departments')),
    )
    create_table(
        'users',
        Column('primary_uuid', POSTGRESQL_UUID, server_default=text('gen_random_uuid()'), nullable=False),
        Column('login', String(length=200), nullable=False),
        Column('full_name', String(length=1000), nullable=False),
        Column('password', String(length=500), nullable=False),
        Column('ip_v4', String(length=15), nullable=True),
        Column('is_active', Boolean(), nullable=True),
        Column('create_at', POSTGRESQL_DATETIME(timezone=True), nullable=True),
        Column('department_id', POSTGRESQL_UUID, nullable=True),
        ForeignKeyConstraint(('department_id', ), ['departments.primary_uuid'], name='fk_users_departments_primary_uuid_department_id'),
        PrimaryKeyConstraint('primary_uuid', name=_alembic_f('pk__users')),
        UniqueConstraint('login', name=_alembic_f('uq__users__login')),
    )
    create_table(
        'sessions',
        Column('primary_uuid', POSTGRESQL_UUID, server_default=text('gen_random_uuid()'), nullable=False),
        Column('login_ts', POSTGRESQL_DATETIME(timezone=True), nullable=False),
        Column('logout_ts', POSTGRESQL_DATETIME(timezone=True), nullable=True),
        Column('user_id', POSTGRESQL_UUID, nullable=False),
        ForeignKeyConstraint(['user_id'], ['users.primary_uuid'], name='fk_sessions_users_primary_uuid_user_id'),
        PrimaryKeyConstraint('primary_uuid', name=_alembic_f('pk__sessions')),
    )
    create_table(
        'conversations',
        Column('primary_uuid', POSTGRESQL_UUID, server_default=text('gen_random_uuid()'), nullable=False),
        Column('start_ts', POSTGRESQL_DATETIME(timezone=True), nullable=False),
        Column('end_ts', POSTGRESQL_DATETIME(timezone=True), nullable=True),
        Column('selected_lang', String(length=30), nullable=True),
        Column('questionare', JSON(), nullable=True),
        Column('session_id', POSTGRESQL_UUID, nullable=False),
        ForeignKeyConstraint(['session_id'], ['sessions.primary_uuid'], name='fk_conversations_sessions_primary_uuid_session_id'),
        PrimaryKeyConstraint('primary_uuid', name=_alembic_f('pk__conversations')),
    )
    create_table(
        'texts',
        Column('primary_uuid', POSTGRESQL_UUID, server_default=text('gen_random_uuid()'), nullable=False),
        Column('create_ts', POSTGRESQL_DATETIME(timezone=True), nullable=True),
        Column('edit_ts', POSTGRESQL_DATETIME(timezone=True), nullable=True),
        Column('audio_raw', LargeBinary(length=104857600), nullable=True),
        Column('lang_from', String(length=30), nullable=False),
        Column('lang_to', String(length=30), nullable=False),
        Column('recognized_text', Text(), nullable=False),
        Column('translated_text', Text(), nullable=False),
        Column('fixed_text', Text(), nullable=True),
        Column('type', String(length=30), nullable=False),
        Column('conversation_id', POSTGRESQL_UUID, nullable=False),
        ForeignKeyConstraint(['conversation_id'], ['conversations.primary_uuid'], name='fk_texts_conversations_primary_uuid_conversation_id'),
        PrimaryKeyConstraint('primary_uuid', name=_alembic_f('pk__texts')),
    )
    # ### end Alembic commands ###

#####################################################################################################

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    drop_table('texts')
    drop_table('conversations')
    drop_table('sessions')
    drop_table('users')
    drop_table('departments')
    # ### end Alembic commands ###

#####################################################################################################
