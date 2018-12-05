from flask import Flask
from flask_restful import Api

import os

#local import
from .api.v1 import v1
from .api.v2.incidents import v2

#from .database_config import create_tables

def create_app(config_name=os.getenv('APP-SETTINGS')):
    app = Flask(__name__)
    #create_tables()
    app.register_blueprint(v1)
    app.register_blueprint(v2)
    return app 