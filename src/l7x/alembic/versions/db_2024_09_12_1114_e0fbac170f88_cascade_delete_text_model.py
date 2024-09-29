#####################################################################################################
"""cascade_delete_text_model

Revision ID: e0fbac170f88
Revises: c38f2590159a
Create Date: 2024-09-12 11:14:40.515565+00:00

"""
#####################################################################################################

from collections.abc import Sequence
from typing import Final

from alembic import op

#####################################################################################################

# revision identifiers, used by Alembic.
# pylint: disable=invalid-name
revision: Final[str] = 'e0fbac170f88'
down_revision: Final[str | None] = 'c38f2590159a'
branch_labels: Final[Sequence[str] | None] = None
depends_on: Final[str | None] = None
# pylint: enable=invalid-name

#####################################################################################################

def upgrade() -> None:
    op.drop_constraint('fk_texts_conversations_primary_uuid_conversation_id', 'texts', type_='foreignkey')
    op.create_foreign_key('fk_texts_conversations_primary_uuid_conversation_id', 'texts', 'conversations', ['conversation_id'], ['primary_uuid'], ondelete='CASCADE')

#####################################################################################################

def downgrade() -> None:
    op.drop_constraint('fk_texts_conversations_primary_uuid_conversation_id', 'texts', type_='foreignkey')
    op.create_foreign_key('fk_texts_conversations_primary_uuid_conversation_id', 'texts', 'conversations', ['conversation_id'], ['primary_uuid'])

#####################################################################################################
