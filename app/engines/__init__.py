import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from app.config import load_config

SQLITE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/resources/' + 'sqlite.db'

SQLITE_URL = 'sqlite:///' + SQLITE_PATH


class DBEngine:

    def __init__(self):
        self.engine = create_engine(load_config().SQLALCHEMY_DATABASE_URI, convert_unicode=True,
                                    encoding='utf-8', pool_size=64, max_overflow=0,
                                    pool_recycle=30, pool_timeout=10)
        self.session = self.create_scoped_session()

    def create_scoped_session(self):
        session_maker = sessionmaker(bind=self.engine)
        return scoped_session(session_maker)


class DBSqliteEngine:

    def __init__(self):
        self.engine = create_engine(SQLITE_URL, convert_unicode=True,
                                    encoding='utf-8')
        self.session = self.create_scoped_session()

    def create_scoped_session(self):
        session_maker = sessionmaker(bind=self.engine)
        return scoped_session(session_maker)


db = DBEngine()
sqlite_db = DBSqliteEngine()
