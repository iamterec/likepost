"""empty message

Revision ID: 581c65f86926
Revises: 56bb18e238c9
Create Date: 2019-03-22 00:03:16.619170

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '581c65f86926'
down_revision = '56bb18e238c9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('aditional_data', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'aditional_data')
    # ### end Alembic commands ###
