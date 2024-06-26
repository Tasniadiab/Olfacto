"""perfume note type association cascade delete all

Revision ID: 048605954911
Revises: 129b5acfdbf8
Create Date: 2024-04-08 00:36:43.821635

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '048605954911'
down_revision = '129b5acfdbf8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=110),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.String(length=110),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)

    # ### end Alembic commands ###
