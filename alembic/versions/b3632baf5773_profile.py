"""profile

Revision ID: b3632baf5773
Revises: 68cc9f3338b1
Create Date: 2024-08-29 19:50:57.469239

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b3632baf5773'
down_revision: Union[str, None] = '68cc9f3338b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('talent_profiles',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.Column('location', sa.String(), nullable=False),
    sa.Column('position', sa.String(), nullable=False),
    sa.Column('company', sa.String(), nullable=False),
    sa.Column('link_ru_resume', sa.String(), nullable=False),
    sa.Column('link_eng_resume', sa.String(), nullable=False),
    sa.Column('link_tg_personal', sa.String(), nullable=False),
    sa.Column('link_linkedin', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_talent_profiles'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('talent_profiles')
    # ### end Alembic commands ###
