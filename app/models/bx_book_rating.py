from sqlalchemy import Column, Integer
from sqlalchemy import String
from .base import Base, BaseColumns


class BxBookRating(Base, BaseColumns):
    __tablename__ = "bx_book_ratings"

    book_isbn = Column(String(30), server_default='', index=True)
    user_id = Column(Integer(), index=True)
    book_rating = Column(Integer(), index=True)

