"""add role to message

Revision ID: 1551ef238e53
Revises: 9c11903053bc
Create Date: 2025-07-16 14:46:16.275233

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1551ef238e53'
down_revision: Union[str, Sequence[str], None] = '9c11903053bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('role', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('messages', 'role')
    # ### end Alembic commands ###
