import string
import uuid

from sqlalchemy import Column, TIMESTAMP, func
from sqlalchemy import Unicode
from sqlalchemy.dialects.postgresql import UUID


unicode_string = Unicode(100)


def make_id_uuid(column_name: string, unique=True) -> Column:
    return Column(
            column_name,
            UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
            unique=True,
            nullable=False
        )


create_at_column = Column('created_at', TIMESTAMP, server_default=func.now())
updated_at_column = Column('updated_at', TIMESTAMP, server_default=func.now())
