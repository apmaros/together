from tokenize import String

from sqlalchemy import Column

from model.base import Base
from model.default_columns import make_user_id_fk


class Post(Base):
    __tablename__ = "posts"

    user_id = make_user_id_fk()
    body = Column(String)
    url = Column(String)
