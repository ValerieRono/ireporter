from flask import Flask
from flask_restful import Api

import os

#local import
from .api.v1 import v1

def create_app(config_name=os.getenv('APP-SETTINGS')):
    app = Flask(__name__)
    app.register_blueprint(v1)
    return app 