from flask import Blueprint
from flask_restful import Api

# local import
from app.api.v1.views import MyIncidents, MyIncident


v1 = Blueprint('api-v1', __name__, url_prefix='/api/v1')
api = Api(v1)

# setup API resource routing
api.add_resource(MyIncidents, '/incidents', strict_slashes=False)
api.add_resource(MyIncident, '/incidents/<int:id>', strict_slashes=False)