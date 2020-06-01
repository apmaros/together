import uuid
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID

id_uuid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
