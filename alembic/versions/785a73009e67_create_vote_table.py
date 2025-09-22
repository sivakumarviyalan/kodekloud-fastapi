"""create vote table

Revision ID: 785a73009e67
Revises: 2cfea42df3b1
Create Date: 2025-09-21 23:20:23.438749

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '785a73009e67'
down_revision: Union[str, Sequence[str], None] = '2cfea42df3b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('votes',
                    sa.Column('user_id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('post_id', sa.Integer(), nullable=False, primary_key=True),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('votes')
    pass
