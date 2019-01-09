from flask import Flask, make_response, jsonify
from flask_cors import CORS

# local import
from .api.v1 import v1
from .api.v2 import v2

from instance.config import app_config
from .database_config import create_tables


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    # CORS(app)
    app.config.from_object(app_config[config_name])
    db_url = app.config.get('DATABASE_URL')
    create_tables(url=db_url)
    app.register_blueprint(v1)
    app.register_blueprint(v2)

    @app.errorhandler(403)
    def forbidden(error):
        return make_response(jsonify({
            "status": 403,
            "message": "Forbidden! Authorization required"
        }), 403)

    @app.errorhandler(404)
    def page_not_found(error):
        return make_response(jsonify({
            "status": 404,
            "message": "not found"
        }), 404)

    @app.errorhandler(500)
    def internal_server_error(error):
        return make_response(jsonify({
            "status": 500,
            "message": "server encountered internal server error"
        }), 500)

    return app