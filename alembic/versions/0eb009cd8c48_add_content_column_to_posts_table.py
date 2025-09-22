"""add content column to posts table

Revision ID: 0eb009cd8c48
Revises: ec6aca637efb
Create Date: 2025-09-21 22:47:16.222567

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0eb009cd8c48'
down_revision: Union[str, Sequence[str], None] = 'ec6aca637efb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    # op.drop_column('posts', 'content')
    pass
