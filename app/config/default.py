# coding: utf-8
import os
from constant import C_PG_DB, C_PG_HOST, C_PG_PASS, C_PG_PORT, C_PG_USER


class Config(object):
    """Base config class."""
    # Flask app config
    DEBUG = True
    # PERMANENT_SESSION_LIFETIME = 7 * 3600 * 24
    SECRET_KEY = "\xb5\xb3}#\xb7A\xcac\x9d0\xb6\x0f\x80z\x97\x00\x1e\xc0\xb8+\xe9)\xf0}"
    PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    SQLALCHEMY_DATABASE_URI = "postgres://postgres:postgres@127.0.0.1/intelligent_bookstore"
    # SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@%s:%s/%s' % \
    #                           (C_PG_USER, C_PG_PASS, C_PG_HOST, C_PG_PORT, C_PG_DB)
    REDIS_PREFIX = "intelligent_bookstore"

    PASSPORT_SERVER = "http://passport.socmap.org/api"
    # session conf
    SESSION_TYPE = "redis"
    SESSION_REDIS = "redis://127.0.0.1/0"
    SESSION_COOKIE_NAME = "intelligent_bookstore"
    # login required
    APP = "intelligent_bookstore"
