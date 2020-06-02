"""create projects table

Revision ID: eefa731ae577
Revises: c85afa0952ed
Create Date: 2020-06-01 20:12:05.732089

"""
import uuid
from alembic import op
import sqlalchemy as sa
# revision identifiers, used by Alembic.
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from db.migration.defaults import (
    make_id_uuid,
    unicode_string,
    make_created_at_column,
    make_updated_at_column
)

revision = 'eefa731ae577'
down_revision = 'c85afa0952ed'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'projects',
        make_id_uuid('id'),
        Column(
            'user_id',
            UUID(as_uuid=True),
            ForeignKey('users.id'),
            primary_key=True,
            default=uuid.uuid4,
            unique=True,
            nullable=False,
        ),
        sa.Column('name', unicode_string, nullable=False),
        sa.Column('description', sa.Unicode(1024), nullable=True),
        sa.Column('purpose', sa.Unicode(255), nullable=False),
        make_created_at_column(),
        make_updated_at_column()
    )


def downgrade():
    op.drop_table('projects')
