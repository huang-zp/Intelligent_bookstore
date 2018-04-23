from sqlalchemy import Column, Integer
from .base import Base, BaseColumns


class BookType(Base, BaseColumns):
    __tablename__ = "booktypes"
    type_id = Column(Integer)
    book_id = Column(Integer)

