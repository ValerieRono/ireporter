from flask import Flask

# local import
from .api.v1 import v1
from .api.v2 import v2

from instance.config import app_config
from .database_config import create_tables


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    db_url = app.config.get('DATABASE_URL')
    create_tables(url=db_url)
    app.register_blueprint(v1)
    app.register_blueprint(v2)

    return app