"""init_database

Revision ID: 9b314d1fd7c9
Revises:
Create Date: 2025-04-17 14:00:36.340324

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9b314d1fd7c9"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "messages",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("client_id", sa.Text, nullable=False),
        sa.Column("type", sa.Text, nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("status", sa.Text, nullable=False),
        sa.Column("timestamp", sa.Text, nullable=False),
    )


def downgrade():
    op.drop_table("messages")
