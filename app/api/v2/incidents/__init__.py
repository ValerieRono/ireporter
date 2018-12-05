""" v2 """
from flask import Blueprint
from flask_restful import Api, Resource 

#local import
from app.api.v2.incidents.views import MyIncidents, MyIncident

v2 = Blueprint('api-v2', __name__, url_prefix='/api/v2')
api = Api(v2)

## setup API resource routing
api.add_resource(MyIncidents, '/incidents', endpoint='incidents')
api.add_resource(MyIncident, '/incidents/<int:id>', endpoint='incident')