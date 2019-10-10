"""empty message

Revision ID: 8ce3576ea3d3
Revises: 6d579362a5ec
Create Date: 2019-10-09 01:42:23.141228

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ce3576ea3d3'
down_revision = '6d579362a5ec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('producer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.UnicodeText(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('movie_producer',
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.Column('producer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.id'], ),
    sa.ForeignKeyConstraint(['producer_id'], ['producer.id'], ),
    sa.PrimaryKeyConstraint('movie_id', 'producer_id')
    )
    op.add_column('url', sa.Column('description', sa.UnicodeText(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('url', 'description')
    op.drop_table('movie_producer')
    op.drop_table('producer')
    # ### end Alembic commands ###
