"""empty message

Revision ID: 9a772e0ae53f
Revises: d29870a556d1
Create Date: 2019-10-01 14:41:49.968423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a772e0ae53f'
down_revision = 'd29870a556d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('document', schema=None) as batch_op:
        batch_op.add_column(sa.Column('address', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('document', schema=None) as batch_op:
        batch_op.drop_column('address')

    # ### end Alembic commands ###
