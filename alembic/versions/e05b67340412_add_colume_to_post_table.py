"""add colume to post table

Revision ID: e05b67340412
Revises: e3e2f6eccf74
Create Date: 2025-05-23 07:37:53.673338

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e05b67340412'
down_revision: Union[str, None] = 'e3e2f6eccf74'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
        op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default="1" ),)
        op.add_column('posts', sa.Column('created_at', sa. TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
        pass


def downgrade() -> None:
    op.drop_column("posts","published")
    op.drop_column("posts","created_at")
    pass
