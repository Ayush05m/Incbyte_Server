"""Add createdAt to User model with default for existing rows

Revision ID: a906e03dc27f
Revises: c6a676d97961
Create Date: 2025-09-24 19:26:42.685705

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a906e03dc27f'
down_revision: Union[str, Sequence[str], None] = 'c6a676d97961'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
