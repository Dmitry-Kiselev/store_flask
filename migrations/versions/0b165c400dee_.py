"""empty message

Revision ID: 0b165c400dee
Revises: 
Create Date: 2017-06-02 12:46:15.655627

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b165c400dee'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=200), nullable=False),
    sa.Column('email', sa.String(length=200), nullable=False),
    sa.Column('password', sa.String(length=120), nullable=False),
    sa.Column('date_joined', sa.DateTime(timezone=True), nullable=False),
    sa.Column('address', sa.String(length=100), nullable=True),
    sa.Column('address_lat', sa.Float(), nullable=True),
    sa.Column('address_lng', sa.Float(), nullable=True),
    sa.Column('authenticated', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
