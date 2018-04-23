from sqlalchemy import Column, Integer, Text
from sqlalchemy import String
from .base import Base, BaseColumns


class Book(Base, BaseColumns):
    __tablename__ = "books"

    title = Column(String(100), server_default='')
    author = Column(String(100), server_default='')
    publisher = Column(String(100), server_default='')
    producer = Column(String(100), server_default='')
    subtitle = Column(String(100), server_default='')
    original_title = Column(String(100), server_default='')
    translator = Column(String(100), server_default='')
    year_of_publisher = Column(String(100), server_default='')
    pages = Column(Text, server_default='')
    price = Column(String(100), server_default='')
    binding = Column(String(100), server_default='')
    series = Column(String(100), server_default='')
    isbn = Column(String(100), server_default='')
    source = Column(String(100), server_default='douban')
    score = Column(String(100), server_default='')
    score_people = Column(String(100), server_default='')
    type = Column(String(100), server_default='')
    content_info = Column(Text, server_default='')
    author_info = Column(Text, server_default='')
    pic_href = Column(Text, server_default='')
