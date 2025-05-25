"""add user table

Revision ID: 812ffd5e47ac
Revises: 05aeddd4db5d
Create Date: 2025-05-23 07:05:24.196221

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '812ffd5e47ac'
down_revision: Union[str, None] = '05aeddd4db5d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(100), nullable=False),
    sa.Column('password', sa.String(100), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
    server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
