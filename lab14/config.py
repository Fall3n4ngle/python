import os

baseDir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
JWT_SECRET_KEY = "screte"

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(baseDir, 'site.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False 
JWT_TOKEN_LOCATION = 'headers'
JWT_ACCESS_TOKEN_EXPIRES = 3600