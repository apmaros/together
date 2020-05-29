"""add timestamps to user

Revision ID: c85afa0952ed
Revises: 28c73584809c
Create Date: 2020-05-02 12:57:19.189989

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import func

revision = 'c85afa0952ed'
down_revision = '28c73584809c'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('users') as batch_op:
        batch_op.add_column(
            sa.Column('created_at', sa.TIMESTAMP, server_default=func.now())
        )
        batch_op.add_column(
            sa.Column('last_access_at', sa.TIMESTAMP, server_default=func.now())
        )


def downgrade():
    with op.batch_alter_table('users') as batch_op:
        batch_op.drop_column('created_at')
        batch_op.drop_column('last_access_at')
