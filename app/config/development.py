# coding: utf-8
from .default import Config
from constant import C_PG_DB, C_PG_HOST, C_PG_PASS, C_PG_PORT, C_PG_USER


class DevelopmentConfig(Config):
    # App config

    SQLALCHEMY_DATABASE_URI = "postgres://postgres:postgres@127.0.0.1/intelligent_bookstore"

