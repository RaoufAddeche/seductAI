"""Ajout table user_scores

Revision ID: daaa9bceb984
Revises: 9b796d3ab38d
Create Date: 2025-07-15 12:10:28.824237

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'daaa9bceb984'
down_revision: Union[str, Sequence[str], None] = '9b796d3ab38d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_scores',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('confiance', sa.Float(), nullable=True),
    sa.Column('clarte', sa.Float(), nullable=True),
    sa.Column('empathie', sa.Float(), nullable=True),
    sa.Column('assertivite', sa.Float(), nullable=True),
    sa.Column('authenticite', sa.Float(), nullable=True),
    sa.Column('creativite', sa.Float(), nullable=True),
    sa.Column('interactions_count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_user_scores_id'), 'user_scores', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_scores_id'), table_name='user_scores')
    op.drop_table('user_scores')
    # ### end Alembic commands ###
