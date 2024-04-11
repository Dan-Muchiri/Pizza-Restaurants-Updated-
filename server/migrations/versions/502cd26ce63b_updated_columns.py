"""updated columns

Revision ID: 502cd26ce63b
Revises: 15a3206dc09f
Create Date: 2024-04-11 10:17:51.232245

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '502cd26ce63b'
down_revision = '15a3206dc09f'
branch_labels = None
depends_on = None


def upgrade():
    # Add the price column to restaurant_pizzas with a default value of 0.0
    op.add_column('restaurant_pizzas', sa.Column('price', sa.Float(), nullable=False, server_default='0.0'))


def downgrade():
    # Drop the price column from restaurant_pizzas
    op.drop_column('restaurant_pizzas', 'price')
