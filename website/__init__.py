from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# create database
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    # create our flask app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SECRET_KEY'   

    # defines where the database is stored
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # initialized the database
    db.init_app(app)
    from .models import User, Post, Comment
    create_database(app)

    # import Blueprints from other files
    from .views import views
    from .auth import auth
    #register the blueprints
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix='/')

    # create login manager (this allows the website to know if a user is logged in)
    login_manager = LoginManager()
    login_manager.view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Create database')
