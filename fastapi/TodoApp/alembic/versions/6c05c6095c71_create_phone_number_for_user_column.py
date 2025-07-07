"""Create phone number for user column

Revision ID: 6c05c6095c71
Revises: 
Create Date: 2025-05-23 13:28:54.781204

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c05c6095c71'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    """Upgrade schema."""


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
