from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from app.services import facade
from flask_bcrypt import bcrypt
from sqlalchemy.exc import IntegrityError

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
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

        try:
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email,
            }, 201
        except IntegrityError:
            return {'error': 'Email already registered'}, 400
        except Exception as e:
            return {'error': str(e)}, 400


    @api.response(200, 'Users retrieved successfully')
    def get(self):
        """Retrieve a list of all users"""
        users = facade.get_all_users()

        if not users:
            return {'message': 'No users found'}, 404

        return [user.to_dict() for user in users], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 201


    @api.expect(user_model, validate=False)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()  # need access token
    def put(self, user_id):
        """Update user details by ID"""
        user_data = api.payload
        current_user = get_jwt_identity()

        if user_id != current_user['id']:
            return {"error": "You are not allowed to update this profile"}

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        if 'email' in user_data or 'password' in user_data:
            return {"error": "You cannot modify email or password"}, 400

        updated_user = facade.update_user(user_id, user_data)
        if not updated_user:
            return {'error': 'User not found'}, 404

        return updated_user.to_dict(), 200
