from flask import Flask
from flask_restful import Api

#local import
from .api.v1 import v1

def create_app():
    app = Flask(__name__)
    app.register_blueprint(v1)
    return app 