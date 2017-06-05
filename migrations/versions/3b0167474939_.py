"""empty message

Revision ID: 3b0167474939
Revises: 904b52de7998
Create Date: 2017-06-05 14:23:00.836742

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b0167474939'
down_revision = '904b52de7998'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('discounts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('value', sa.DECIMAL(), nullable=True),
    sa.Column('in_percent', sa.Boolean(), nullable=True),
    sa.Column('available_from', sa.DateTime(), nullable=True),
    sa.Column('available_until', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('basket_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.Column('discount_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['basket_id'], ['baskets.id'], ),
    sa.ForeignKeyConstraint(['discount_id'], ['discounts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('charge_id', sa.String(length=200), nullable=False),
    sa.Column('charged_sum', sa.DECIMAL(), nullable=True),
    sa.Column('discount_sum', sa.DECIMAL(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('charge_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payments')
    op.drop_table('orders')
    op.drop_table('discounts')
    # ### end Alembic commands ###
