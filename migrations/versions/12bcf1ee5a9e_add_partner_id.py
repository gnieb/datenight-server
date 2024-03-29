"""add partner id

Revision ID: 12bcf1ee5a9e
Revises: 1968b1d67c1a
Create Date: 2024-01-06 21:03:39.591801

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12bcf1ee5a9e'
down_revision = '1968b1d67c1a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('partner_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'users', ['partner_id'], ['id'], ondelete='SET NULL')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('partner_id')

    # ### end Alembic commands ###
