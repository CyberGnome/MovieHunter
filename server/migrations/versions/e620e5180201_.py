"""empty message

Revision ID: e620e5180201
Revises: e14eac0696da
Create Date: 2019-10-09 18:07:49.694231

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e620e5180201'
down_revision = 'e14eac0696da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('created', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'created')
    # ### end Alembic commands ###
