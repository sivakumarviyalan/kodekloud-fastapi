"""add user table

Revision ID: 09b6ae70ea6a
Revises: 0eb009cd8c48
Create Date: 2025-09-21 22:53:25.883596

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '09b6ae70ea6a'
down_revision: Union[str, Sequence[str], None] = '0eb009cd8c48'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('email', sa.String(), nullable=False, unique=True),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
