"""initial migration

Revision ID: 487210a9c40b
Revises: 
Create Date: 2023-10-21 11:47:11.905019

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '487210a9c40b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('property',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=500), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.Column('rent', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('property', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_property_address'), ['address'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('property', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_property_address'))

    op.drop_table('property')
    # ### end Alembic commands ###