"""Added perfume relationship to Notes model

Revision ID: 7d8a626c129d
Revises: 950ac728dde0
Create Date: 2024-04-06 03:54:55.208916

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d8a626c129d'
down_revision = '950ac728dde0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notes', schema=None) as batch_op:
        batch_op.drop_column('test')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('test', sa.TEXT(), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
