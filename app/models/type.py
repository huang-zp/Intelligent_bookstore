from sqlalchemy import Column, Integer, Text
from sqlalchemy import String
from .base import Base, BaseColumns


class Type(Base, BaseColumns):
    __tablename__ = "types"
    title = Column(String(100), server_default='')

