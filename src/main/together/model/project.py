import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from model.base import Base
from model.default_columns import make_id_fk


class Project(Base):
    __tablename__ = "projects"

    user_id = make_id_fk()
    name = Column(String)
    description = Column(String)
    purpose = Column(String)
