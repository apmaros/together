from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.orm import relationship
from model.base import Base


class User(Base):
    __tablename__ = "users"

    username = Column(String)
    email = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    created_at = Column(TIMESTAMP)
    last_access_at = Column(TIMESTAMP)

    # Relationships
    projects = relationship('Project')

    def __repr__(self):
        return "<User(username='%s', email='%s')>" % (
            self.username,
            self.email
        )
