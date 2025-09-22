"""add last few columns to posts table

Revision ID: 2cfea42df3b1
Revises: 1f6a11174803
Create Date: 2025-09-21 23:11:21.185871

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2cfea42df3b1'
down_revision: Union[str, Sequence[str], None] = '1f6a11174803'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
