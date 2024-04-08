"""perfume note type association deleted

Revision ID: 129b5acfdbf8
Revises: 30ccb2d66002
Create Date: 2024-04-07 13:23:23.299190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '129b5acfdbf8'
down_revision = '30ccb2d66002'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notes_note_type')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notes_note_type',
    sa.Column('note_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('note_type_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['note_id'], ['notes.id'], name='notes_note_type_note_id_fkey'),
    sa.ForeignKeyConstraint(['note_type_id'], ['note_types.id'], name='notes_note_type_note_type_id_fkey'),
    sa.PrimaryKeyConstraint('note_id', 'note_type_id', name='notes_note_type_pkey')
    )
    # ### end Alembic commands ###