# coding: utf-8

import os

import sys


from flask import Flask, jsonify, request, g, json


project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_path not in sys.path:
    sys.path.insert(0, project_path)


def create_app():
    """Create Flask app."""

    app = Flask(__name__)
    config_app(app)
    # Register components

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