"""add col confirmed_at to resume table

Revision ID: 1f9d42f726f9
Revises: b8d11b79170c
Create Date: 2021-12-06 19:21:52.478418

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f9d42f726f9'
down_revision = 'b8d11b79170c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('resume', sa.Column('confirmed_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('resume', 'confirmed_at')
    # ### end Alembic commands ###
