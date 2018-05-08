
from sqlalchemy import Column, Text, String
from .base import Base, BaseColumns
from flask_security import RoleMixin


class Log(Base, BaseColumns, RoleMixin):
    __tablename__ = "logs"

    user = Column(String(50), server_default='')
    operate = Column(String(100), server_default='')


