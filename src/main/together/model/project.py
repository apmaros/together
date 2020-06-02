import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from model.base import Base


class Project(Base):
    __tablename__ = "projects"

    user_id = Column(
        ForeignKey('users.id'),
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column(String)
    description = Column(String)
    purpose = Column(String)
