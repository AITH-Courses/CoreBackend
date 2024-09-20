"""playlists

Revision ID: e29544b891d8
Revises: 3b078e034715
Create Date: 2024-09-19 15:05:33.287189

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e29544b891d8'
down_revision: Union[str, None] = '3b078e034715'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('playlists',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('course_run_id', sa.Uuid(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('link', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.PrimaryKeyConstraint('id', 'course_run_id', name=op.f('pk_playlists'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('playlists')
    # ### end Alembic commands ###
