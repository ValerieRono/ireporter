from flask import Flask
from flask_restful import Api

import os

# local import
from .api.v1 import v1
from .api.v2 import v2


# from ..instance.config import app_config
from .database_config import create_tables


def create_app(config_name):
    app = Flask(__name__)
    create_tables()
    app.register_blueprint(v1)
    app.register_blueprint(v2)
    # app.config.from_object(app_config[config_name])
    # app.config.from_pyfile('config.py')

    return app 