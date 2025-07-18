"""add agents_used

Revision ID: e87ed045cca6
Revises: 8c361280e465
Create Date: 2025-07-09 22:35:25.032410

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e87ed045cca6'
down_revision: Union[str, Sequence[str], None] = '8c361280e465'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('interactions', sa.Column('agents_used', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('interactions', 'agents_used')
    # ### end Alembic commands ###
