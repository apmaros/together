from tokenize import String

from sqlalchemy import Column

from model.base import Base
from model.default_columns import user_id_foreign_key


class Post(Base):
    __tablename__ = "posts"

    user_id = user_id_foreign_key
    body = Column(String)
    url = Column(String)
