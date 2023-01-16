from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Create a database object
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecretkey'
    # Telling flask that the database is located at this location
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # Setup database
    db.init_app(app)

    # Tell flask we have blueprints made
    from .views import views
    from .auth import auth

    # Register blueprints with application
    app.register_blueprint(views, url_prefix="/")  # / means no prefix
    # Otherwise if we do /auth here then any route in auth.py will have the prefix auth/[nameOfRoute]
    app.register_blueprint(auth, url_prefix="/")

    # From the models.py we need to run this file before we create our database
    from .models import User, Note

    create_database(app)

    # Init Login manager
    login_manager = LoginManager()
    # Where should we be directed if not logged in
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # This is telling flask how do we load a user, use this function
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app

# This will create a database if it does not already exist


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')
