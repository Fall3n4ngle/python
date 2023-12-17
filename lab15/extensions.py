from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import JWTManager
from flask_restful import Api 
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
bcrypt = Bcrypt()
auth = HTTPBasicAuth()
jwt = JWTManager()
api = Api() 
ma = Marshmallow()