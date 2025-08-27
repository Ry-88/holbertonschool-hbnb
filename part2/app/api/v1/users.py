from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email}, 201
    
    @api.response(200, 'List of users')
    def get(self):
        """Get all users"""
        users = facade.get_all_users()
        return [
            {
                'id': u.id,
                'first_name': u.first_name,
                'last_name': u.last_name,
                'email': u.email
            } for u in users
        ], 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

@api.route('/<int:user_id>')
class UserUpdate(Resource):
    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update an existing user"""
        user_data = api.payload

        # validate
        existing_user = facade.get_user_by_id(user_id)
        if not existing_user:
            return {'error': 'User not found'}, 404

        # update
        updated_user = facade.update_user(user_id, user_data)

        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200

















    # from flask import request
    # from flask_restx import Namespace, Resource, fields
    # from ..services import users as svc

    # ns = Namespace("users", description="User management")

    # user_out = ns.model("User", {
    #     "id": fields.String,
    #     "email": fields.String,
    #     "first_name": fields.String,
    #     "last_name": fields.String,
    #     "created_at": fields.String,
    #     "updated_at": fields.String,
    # })

    # user_in = ns.model("UserCreate", {
    #     "email": fields.String(required=True),
    #     "password": fields.String(required=True),
    #     "first_name": fields.String,
    #     "last_name": fields.String,
    # })

    # user_upd = ns.model("UserUpdate", {
    #     "email": fields.String,
    #     "password": fields.String,
    #     "first_name": fields.String,
    #     "last_name": fields.String,
    # })

    # @ns.route("/")
    # class UserList(Resource):
    #     @ns.marshal_list_with(user_out, code=200, description="List of users")
    #     def get(self):
    #         body, status = svc.list_users()
    #         return body, status

    #     @ns.expect(user_in, validate=True)
    #     @ns.marshal_with(user_out, code=201, description="User created")
    #     def post(self):
    #         data = request.get_json() or {}
    #         body, status = svc.create_user(data)
    #         return body, status

    # @ns.route("/<string:user_id>")
    # @ns.param("user_id", "User identifier")
    # class UserItem(Resource):
    #     @ns.marshal_with(user_out, code=200, description="User by id")
    #     def get(self, user_id):
    #         body, status = svc.get_user(user_id)
    #         return body, status

    #     @ns.expect(user_upd, validate=True)
    #     @ns.marshal_with(user_out, code=200, description="User updated")
    #     def put(self, user_id):
    #         data = request.get_json() or {}
    #         if not any(k in data for k in ("email", "password", "first_name", "last_name")):
    #             return {"error": "No updatable fields provided"}, 400
    #         body, status = svc.update_user(user_id, data)
    #         return body, status
