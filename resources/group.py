from flask_restful import Resource, reqparse
from models.user import GroupModel


class GroupsList(Resource):
    def get(self):
        return {'groups': [g.json() for g in GroupModel.query.all()]}


class Groups(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="This field cannot be blank")
    parser.add_argument('description', type=str, required=False)

    def get(self, _id):
        group = GroupModel.find_by_id(_id)
        if not group:
            return {"message": "Group not found"}, 404
        return group.json()

    def post(self):
        data = Groups.parser.parse_args()
        group = GroupModel(data['name'], data['description'])
        msg = group.save_to_db()
        if msg:
            return msg, 500
        return {"message": "Group created successfully", "group": group.json()}, 201

    def put(self):
        pass

    def delete(self):
        pass