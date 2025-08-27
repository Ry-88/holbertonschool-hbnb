from flask import request
from flask_restx import Namespace, Resource, fields
from ..services import users as svc

ns = Namespace("users", description="User management")

user_out = ns.model("User", {
    "id": fields.String,
    "email": fields.String,
    "first_name": fields.String,
    "last_name": fields.String,
    "created_at": fields.String,
    "updated_at": fields.String,
})

user_in = ns.model("UserCreate", {
    "email": fields.String(required=True),
    "password": fields.String(required=True),
    "first_name": fields.String,
    "last_name": fields.String,
})

user_upd = ns.model("UserUpdate", {
    "email": fields.String,
    "password": fields.String,
    "first_name": fields.String,
    "last_name": fields.String,
})

@ns.route("/")
class UserList(Resource):
    @ns.marshal_list_with(user_out, code=200, description="List of users")
    def get(self):
        body, status = svc.list_users()
        return body, status

    @ns.expect(user_in, validate=True)
    @ns.marshal_with(user_out, code=201, description="User created")
    def post(self):
        data = request.get_json() or {}
        body, status = svc.create_user(data)
        return body, status

@ns.route("/<string:user_id>")
@ns.param("user_id", "User identifier")
class UserItem(Resource):
    @ns.marshal_with(user_out, code=200, description="User by id")
    def get(self, user_id):
        body, status = svc.get_user(user_id)
        return body, status

    @ns.expect(user_upd, validate=True)
    @ns.marshal_with(user_out, code=200, description="User updated")
    def put(self, user_id):
        data = request.get_json() or {}
        if not any(k in data for k in ("email", "password", "first_name", "last_name")):
            return {"error": "No updatable fields provided"}, 400
        body, status = svc.update_user(user_id, data)
        return body, status
