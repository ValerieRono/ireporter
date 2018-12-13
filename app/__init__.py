from flask import Flask

# local import
from .api.v1 import v1
from .api.v2 import v2

from .database_config import create_tables

def create_app(config_name):
    app = Flask(__name__)
    create_tables()
    
    app.register_blueprint(v1)
    app.register_blueprint(v2)
    
    return app 