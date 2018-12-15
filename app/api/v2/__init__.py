""" v2 """
from flask import Blueprint
from flask_restful import Api

# local import
from app.api.v2.incidents.views import MyIncidents, MyIncident
from app.api.v2.Users.views import MyUsers, MyUser, login

v2 = Blueprint('api-v2', __name__, url_prefix='/api/v2')
api = Api(v2)

# setup API resource routing
api.add_resource(MyIncidents, '/incidents', endpoint='incidents')
api.add_resource(MyIncident, '/incidents/<int:id>', endpoint='new_incident')

api.add_resource(MyUsers, '/users', endpoint='users')
api.add_resource(MyUser, '/users/<int:id>', endpoint='user')
api.add_resource(login, '/user', endpoint='login')
