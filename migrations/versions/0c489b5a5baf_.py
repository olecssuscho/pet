"""empty message

Revision ID: 0c489b5a5baf
Revises: b4a4981e056b
Create Date: 2026-05-13 14:34:54.762513

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c489b5a5baf'
down_revision: Union[str, Sequence[str], None] = 'b4a4981e056b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
