from sqlalchemy import Column, Integer
from sqlalchemy import String
from .base import Base, BaseColumns


class User(Base, BaseColumns):
    __tablename__ = "users"

    location = Column(String(100), server_default='', index=True)
    age = Column(Integer(), index=True)

    name = Column(String(50), server_default='')  # 用户名

    email = Column(String(100), server_default='')   # 用户邮箱

    role_id = Column(Integer(), server_default='0')   # 用户角色ID

    active = Column(Integer, server_default='0')   # 用户是否激活
    password = Column(String(100), server_default='')   # 用户密码

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.name
