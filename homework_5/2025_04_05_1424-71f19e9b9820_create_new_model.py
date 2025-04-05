"""Create new model

Revision ID: 71f19e9b9820
Revises: 11c5ae697267
Create Date: 2025-04-05 14:24:24.386280

"""
from alembic import op
import sqlalchemy as sa



revision = '71f19e9b9820'
down_revision = '11c5ae697267'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('categories',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=75), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('questions', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'categories', ['category_id'], ['id'])



def downgrade():
    with op.batch_alter_table('questions', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    op.drop_table('categories')

