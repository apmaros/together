import string
import uuid

from sqlalchemy import Column, TIMESTAMP, func, ForeignKey
from sqlalchemy import Unicode
from sqlalchemy.dialects.postgresql import UUID

# type
unicode_string = Unicode(100)


# column
def make_id_uuid(column_name: string, is_unique=True) -> Column:
    return Column(
            column_name,
            UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
            unique=is_unique,
            nullable=False
        )


def make_id_fk_column(column_name: string = 'users') -> Column:
    return Column(
            f'{column_name}_id',
            UUID(as_uuid=True),
            ForeignKey(f'{column_name}.id'),
            primary_key=False,
            default=uuid.uuid4,
            unique=True,
            nullable=False,
        )


def make_created_at_column() -> Column:
    return Column('created_at', TIMESTAMP, server_default=func.now())


def make_updated_at_column() -> Column:
    return Column('updated_at', TIMESTAMP, server_default=func.now())
