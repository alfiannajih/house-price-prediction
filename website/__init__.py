from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask_login import LoginManager

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from . import models
    with app.app_context():
        db.create_all()

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for main
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # blueprint for predict_price
    from .predict_price import predict_price as predict_price_blueprint
    app.register_blueprint(predict_price_blueprint)

    return app