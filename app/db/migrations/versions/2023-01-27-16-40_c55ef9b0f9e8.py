"""add_user_table

Revision ID: c55ef9b0f9e8
Revises: 
Create Date: 2023-01-27 16:40:20.728374

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op


# revision identifiers, used by Alembic.
revision = 'c55ef9b0f9e8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('username', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('id', sqlmodel.sql.sqltypes.GUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('fist_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column('last_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=True)


def downgrade():
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
