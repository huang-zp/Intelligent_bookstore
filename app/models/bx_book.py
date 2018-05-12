from sqlalchemy import Column, Text
from sqlalchemy import String
from .base import Base, BaseColumns


class BxBook(Base, BaseColumns):
    __tablename__ = "bx_books"

    book_isbn = Column(String(100), server_default='', index=True)
    book_title = Column(String(300), server_default='')
    book_author = Column(String(300), server_default='')
    book_year_of_publication = Column(String(30), server_default='')
    book_publisher = Column(String(300), server_default='')
    book_image_url_s = Column(Text, server_default='')
    book_image_url_m = Column(Text, server_default='')
    book_image_url_l = Column(Text, server_default='')

