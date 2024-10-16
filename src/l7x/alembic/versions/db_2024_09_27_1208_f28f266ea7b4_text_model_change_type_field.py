#####################################################################################################
"""text-model-change-type-field

Revision ID: f28f266ea7b4
Revises: 92e150428401
Create Date: 2024-09-27 12:08:49.452518+00:00

"""
#####################################################################################################

from collections.abc import Sequence
from typing import Final

import sqlalchemy as sa
from alembic import op
from sqlalchemy.databases import postgres

#####################################################################################################

# revision identifiers, used by Alembic.
# pylint: disable=invalid-name
revision: Final[str] = 'f28f266ea7b4'
down_revision: Final[str | None] = '92e150428401'
branch_labels: Final[Sequence[str] | None] = None
depends_on: Final[str | None] = None
# pylint: enable=invalid-name

#####################################################################################################

def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('texts', sa.Column('owner_session_uuid', postgres.UUID(), nullable=True))
    op.create_foreign_key('fk_texts_sessions_primary_uuid_owner_session_uuid', 'texts', 'sessions', ['owner_session_uuid'], ['primary_uuid'], ondelete='SET NULL')
    op.drop_column('texts', 'type')
    # ### end Alembic commands ###

#####################################################################################################

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('texts', sa.Column('type', sa.VARCHAR(length=30), autoincrement=False, nullable=False))
    op.drop_constraint('fk_texts_sessions_primary_uuid_owner_session_uuid', 'texts', type_='foreignkey')
    op.drop_column('texts', 'owner_session_uuid')
    # ### end Alembic commands ###

#####################################################################################################
