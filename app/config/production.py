from .default import Config
from constant import C_PG_DB, C_PG_HOST, C_PG_PASS, C_PG_PORT, C_PG_USER


class ProductionConfig(Config):
    # App config

    DEBUG = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@%s:%s/%s' % \
                              (C_PG_USER, C_PG_PASS, C_PG_HOST, C_PG_PORT, C_PG_DB)

