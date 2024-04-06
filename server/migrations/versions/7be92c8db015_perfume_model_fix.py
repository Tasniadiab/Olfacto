"""Perfume model fix

Revision ID: 7be92c8db015
Revises: 5d1333c82c14
Create Date: 2024-04-06 14:29:12.262106

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7be92c8db015'
down_revision = '5d1333c82c14'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('brands', schema=None) as batch_op:
        batch_op.alter_column('logo',
               existing_type=postgresql.BYTEA(),
               type_=sa.String(length=300),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('brands', schema=None) as batch_op:
        batch_op.alter_column('logo',
               existing_type=sa.String(length=300),
               type_=postgresql.BYTEA(),
               existing_nullable=True)

    # ### end Alembic commands ###
