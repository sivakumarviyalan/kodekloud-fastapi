"""add foreign-key to posts table

Revision ID: 1f6a11174803
Revises: 09b6ae70ea6a
Create Date: 2025-09-21 23:02:12.133109

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f6a11174803'
down_revision: Union[str, Sequence[str], None] = '09b6ae70ea6a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', 
                          local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
