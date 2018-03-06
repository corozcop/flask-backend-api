from models import CustomerModel
from flask_restful import Resource


class CustomerList(Resource):
    def get(self):
        return {'customer': [g.json() for g in CustomerModel.query.all()]}
