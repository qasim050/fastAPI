"""add content colum

Revision ID: 05aeddd4db5d
Revises: 4334dbcb9170
Create Date: 2025-05-23 06:54:19.464571

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '05aeddd4db5d'
down_revision: Union[str, None] = '4334dbcb9170'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("content",sa.String(1000),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts","content")
    pass
