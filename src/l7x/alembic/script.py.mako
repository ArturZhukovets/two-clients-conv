<%text>#####################################################################################################</%text>
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
<%text>#####################################################################################################</%text>

from collections.abc import Sequence
from typing import Final

import sqlalchemy as sa
from alembic import op
${imports if imports else ""}

<%text>#####################################################################################################</%text>

# revision identifiers, used by Alembic.
# pylint: disable=invalid-name
revision: Final[str] = ${repr(up_revision)}
down_revision: Final[str | None] = ${repr(down_revision)}
branch_labels: Final[Sequence[str] | None] = ${repr(branch_labels)}
depends_on: Final[str | None] = ${repr(depends_on)}
# pylint: enable=invalid-name

<%text>#####################################################################################################</%text>

def upgrade() -> None:
    ${upgrades if upgrades else '"""DO NOTHING."""'}

<%text>#####################################################################################################</%text>

def downgrade() -> None:
    ${downgrades if downgrades else '"""DO NOTHING."""'}

<%text>#####################################################################################################</%text>
