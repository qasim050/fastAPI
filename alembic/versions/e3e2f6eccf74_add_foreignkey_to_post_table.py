"""add foreignkey to post table

Revision ID: e3e2f6eccf74
Revises: 812ffd5e47ac
Create Date: 2025-05-23 07:16:37.733514

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e3e2f6eccf74'
down_revision: Union[str, None] = '812ffd5e47ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("owner_id",sa.Integer(),nullable=False))
    op.create_foreign_key("post_users_fk",source_table="posts",referent_table="users",local_cols=["owner_id"],remote_cols=["id"],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("post_users_fk",table_name="posts", type_="foreignkey")
    op.drop_column("posts","owner_id")
    pass
