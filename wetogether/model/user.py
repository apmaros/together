import uuid

from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID

from model.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    username = Column(String)
    email = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    created_at = Column(TIMESTAMP)
    last_access_at = Column(TIMESTAMP)

    def __repr__(self):
        return "<User(username='%s', email='%s')>" % (
            self.username,
            self.email
        )
