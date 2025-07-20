"""
Add username, email_verified, and role_id to User

Revision ID: add_username_email_verified_role_to_user
Revises: 31349c15d713
Create Date: 2025-07-20
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=50), unique=True, nullable=True))
        batch_op.add_column(sa.Column('email_verified', sa.Boolean(), nullable=False, server_default='0'))
        batch_op.add_column(sa.Column('role_id', sa.Integer(), nullable=True))
        # If using SQLite, you may need to manually add foreign key
    op.create_table(
        'user_role',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=50), unique=True, nullable=False),
        sa.Column('description', sa.String(length=255)),
    )

def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('username')
        batch_op.drop_column('email_verified')
        batch_op.drop_column('role_id')
    op.drop_table('user_role')
