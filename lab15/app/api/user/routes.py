from flask import Blueprint
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_marshmallow import Marshmallow
from extensions import db
from app.auth.models import User

user_bp = Blueprint('api_user', __name__)
api = Api(user_bp)

ma = Marshmallow(user_bp)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'image_file': fields.String,
    'password': fields.String,
    'about_me': fields.String,
    'last_seen': fields.DateTime(dt_format='rfc822')
}

class UserResource(Resource):
    @marshal_with(user_fields)
    def get(self, id):
        user = User.query.get(id)
        if not user:
            abort(404, message="User {} doesn't exist".format(id))
        return user

    @marshal_with(user_fields)
    def put(self, id):
        parsed_args = user_schema.load(reqparse.RequestParser().parse_args())
        user = User.query.get(id)
        user.username = parsed_args['username']
        user.email = parsed_args['email']
        db.session.add(user)
        db.session.commit()
        return user, 201

    def delete(self, id):
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return {}, 204

class UserListResource(Resource):
    @marshal_with(user_fields)
    def get(self):
        users = User.query.all()
        return users

    @marshal_with(user_fields)
    def post(self):
        parsed_args = user_schema.load(reqparse.RequestParser().parse_args())
        user = User(username=parsed_args['username'], email=parsed_args['email'])
        db.session.add(user)
        db.session.commit()
        return user, 201

api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:id>')
