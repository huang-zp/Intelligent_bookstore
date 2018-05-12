# coding: utf-8
import logging
import os
import pkgutil
import sys
from logging.handlers import TimedRotatingFileHandler
from app.models import User, Role
from app.engines import db
from flask import Flask, jsonify, request, g, json
from app.controllers import ib , auth, book_operate, user_operate, log_operate, info, rating_operate, front_index

from flask_login import LoginManager
# from app.cache import cache

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_path not in sys.path:
    sys.path.insert(0, project_path)


def create_app():
    """Create Flask app."""

    app = Flask(__name__)
    config_app(app)
    login_manager = LoginManager()
    login_manager.session_protection = 'strong'
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)
    # Register components
    # app.register_blueprint(infomation)
    # app.register_blueprint(vulner)

    app.register_blueprint(ib)
    app.register_blueprint(auth)
    app.register_blueprint(book_operate)
    app.register_blueprint(user_operate)
    app.register_blueprint(log_operate)

    app.register_blueprint(info)
    app.register_blueprint(rating_operate)
    app.register_blueprint(front_index)
    # cache.init_app(app)

    class NonASCIIJsonEncoder(json.JSONEncoder):
        def __init__(self, **kwargs):
            kwargs['ensure_ascii'] = False
            super(NonASCIIJsonEncoder, self).__init__(**kwargs)

    app.json_encoder = NonASCIIJsonEncoder

    return app


def config_app(app):
    from .config import load_config
    config = load_config()

    app.config.from_object(config)



