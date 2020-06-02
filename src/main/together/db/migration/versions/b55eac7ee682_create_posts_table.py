"""create posts table

Revision ID: b55eac7ee682
Revises: eefa731ae577
Create Date: 2020-06-02 21:15:56.988816

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import Column

from db.migration.defaults import (
    make_id_uuid,
    unicode_string,
    make_created_at_column,
    make_updated_at_column,
    make_user_id_fk_column
)

revision = 'b55eac7ee682'
down_revision = 'eefa731ae577'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'posts',
        make_id_uuid('id'),
        make_user_id_fk_column(),
        Column('body', unicode_string, nullable=False),
        Column('url', unicode_string, nullable=False),
        make_created_at_column(),
        make_updated_at_column()
    )


def downgrade():
    op.drop_table('posts')
