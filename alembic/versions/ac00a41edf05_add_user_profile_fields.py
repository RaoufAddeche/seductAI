"""add user profile fields

Revision ID: ac00a41edf05
Revises: 574eed4befc1
Create Date: 2025-07-15 10:20:01.475191

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ac00a41edf05'
down_revision: Union[str, Sequence[str], None] = '574eed4befc1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('age', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('gender', sa.String(), nullable=True))
    op.add_column('users', sa.Column('orientation', sa.String(), nullable=True))
    op.add_column('users', sa.Column('style_langage', sa.String(), nullable=True))
    op.add_column('users', sa.Column('centre_interets', postgresql.ARRAY(sa.String()), nullable=True))
    op.add_column('users', sa.Column('situation', sa.String(), nullable=True))
    op.add_column('users', sa.Column('classe', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'classe')
    op.drop_column('users', 'situation')
    op.drop_column('users', 'centre_interets')
    op.drop_column('users', 'style_langage')
    op.drop_column('users', 'orientation')
    op.drop_column('users', 'gender')
    op.drop_column('users', 'age')
    # ### end Alembic commands ###
