"""create users table

Revision ID: 590514a18400
Revises:
Create Date: 2020-04-12 17:48:55.676172

"""
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy.dialects.postgresql import UUID

revision = '590514a18400'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column(
            'id',
            UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
            unique=True,
            nullable=False
        ),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('email', sa.Unicode(100), nullable=False),
        sa.Column('first_name', sa.Unicode(100), nullable=True),
        sa.Column('last_name', sa.Unicode(100), nullable=True),
    )


def downgrade():
    op.drop_table('users')
