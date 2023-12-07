from flask import Flask
from extensions import *

from .todo.views import todo
from .feedback.views import feedback
from .portfolio.views import portfolio
from .session.views import sessionBp
from .auth.views import auth
from .auth.models import User
from .category.views import categoryBp
from .post.views import postBp
from .api.routes import api_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    with app.app_context():
        app.register_blueprint(todo, url_prefix="/todo")
        app.register_blueprint(feedback, url_prefix="/feedback")
        app.register_blueprint(portfolio, url_prefix="/portfolio")
        app.register_blueprint(sessionBp, url_prefix="/session")
        app.register_blueprint(auth, url_prefix="/auth")
        app.register_blueprint(categoryBp, url_prefix="/category")
        app.register_blueprint(postBp, url_prefix="/post")
        app.register_blueprint(api_bp, url_prefix="/api")

    return app