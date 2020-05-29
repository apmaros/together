"""add password to user

Revision ID: 28c73584809c
Revises: 590514a18400
Create Date: 2020-05-02 12:39:20.886536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import func

revision = '28c73584809c'
down_revision = '590514a18400'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'users',
        sa.Column('password', sa.String, nullable=False)
    )


def downgrade():
    pass
