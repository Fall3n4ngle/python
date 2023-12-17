from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db, auth
from app.auth.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token


@auth.verify_password
def verify_basic_password(username, password):
    user = User.query.filter_by(username=username).first()

    if user is None:
        return None
    
    if check_password_hash(user.password, password):
        return username


auth_bp = Blueprint('api_auth', __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not "username" in data or not "password" in data or not "email" in data:
        return jsonify({"message": "Provide username and password"}), 401
    
    username = data['username']
    password = data['password']
    email = data['email']

    exist_user = User.query.filter_by(username=username).first()
    if exist_user:
        return jsonify({"message": "User already exists"}), 401
    
    hashed_password = generate_password_hash(password)
    new_user = User(
        username=username,
        email=email,
        password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Registered successfully"})


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not "username" in data or not "password" in data:
        return jsonify({"message": "Provide username and password"}), 401
    
    username = data['username']
    password = data['password']

    if not username or not password:
        return jsonify({"message": "Provide username and password"}), 401
    
    exist_user = User.query.filter_by(username=username).first()
    if not exist_user:
        return jsonify({"message": "User not found"}), 401
    
    if not check_password_hash(exist_user.password, password):
        return jsonify({"message": "Invalid password"}), 401
    
    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity="example_user")
    return jsonify(access_token=access_token, refresh_token=refresh_token)


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)