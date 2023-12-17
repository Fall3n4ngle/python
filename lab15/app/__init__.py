from flask import Flask, send_from_directory
from extensions import *

from .todo.views import todo
from .feedback.views import feedback
from .portfolio.views import portfolio
from .session.views import sessionBp
from .auth.views import auth
from .auth.models import User
from .category.views import categoryBp
from .post.views import postBp
from .api.todo.routes import todo_bp
from .api.auth.routes import auth_bp
from .api.user.routes import user_bp
from .api.swagger.routes import swaggerui_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)

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
        app.register_blueprint(todo_bp, url_prefix="/api")
        app.register_blueprint(auth_bp, url_prefix="/api")
        app.register_blueprint(user_bp, url_prefix="/api")
        app.register_blueprint(swaggerui_blueprint, url_prefix='/api/docs')

        @app.route('/swagger')
        def swagger_json():
            return send_from_directory('../static', 'swagger.json')

    return app