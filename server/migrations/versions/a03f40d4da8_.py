"""empty message

Revision ID: a03f40d4da8
Revises: None
Create Date: 2015-03-21 16:15:29.134901

"""

# revision identifiers, used by Alembic.
revision = 'a03f40d4da8'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('md5', sa.Text(), nullable=True),
    sa.Column('token', sa.Text(), nullable=True),
    sa.Column('tag', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('image')
    ### end Alembic commands ###
