"""empty message

Revision ID: 029cff91ee6d
Revises: ba4ce1cb909d
Create Date: 2019-10-14 22:55:06.438081

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '029cff91ee6d'
down_revision = 'ba4ce1cb909d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('public_id', postgresql.UUID(as_uuid=True), nullable=False))
    op.add_column('user', sa.Column('username', sa.String(length=32), nullable=True))
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=False)
    op.drop_index('ix_user_login', table_name='user')
    op.create_unique_constraint(None, 'user', ['public_id'])
    op.drop_column('user', 'login')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('login', sa.VARCHAR(length=32), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'user', type_='unique')
    op.create_index('ix_user_login', 'user', ['login'], unique=False)
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_column('user', 'username')
    op.drop_column('user', 'public_id')
    # ### end Alembic commands ###
