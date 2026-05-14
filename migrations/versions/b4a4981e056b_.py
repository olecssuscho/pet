"""empty message

Revision ID: b4a4981e056b
Revises: 23498b2a0100
Create Date: 2026-05-09 11:35:53.903898

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b4a4981e056b'
down_revision: Union[str, Sequence[str], None] = '23498b2a0100'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
