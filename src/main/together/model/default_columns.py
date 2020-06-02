import uuid
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

id_uuid = Column(
    UUID(as_uuid=True),
    primary_key=True,
    default=uuid.uuid4,
    unique=True,
    nullable=False,
)


def make_user_id_fk() -> Column:
    return Column(
        ForeignKey('users.id'),
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
