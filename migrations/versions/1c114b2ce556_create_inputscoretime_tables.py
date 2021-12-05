"""create inputscoretime tables

Revision ID: 1c114b2ce556
Revises: c642b0ea5548
Create Date: 2021-12-05 02:18:49.919640

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1c114b2ce556'
down_revision = 'c642b0ea5548'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('inputScoreTime',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('end_date'),
    sa.UniqueConstraint('start_date')
    )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    
    op.drop_table('inputScoreTime')
    # ### end Alembic commands ###
