from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
#libaries imported^
db =SQLAlchemy()
DB_NAME ='database.db'
#database is created
def create_app():
    'Module that creates the Flask application'
    app=Flask(__name__)
    app.config['SECRET_KEY']='Mufat nuts'
    app.config['SQLALCHEMY_DATABASE_URI']= f'sqlite:///{DB_NAME}'
    db.init_app(app)


    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    #registers the blueprients for the templates within views and auth 

    from .models import User
    create_database(app)
    #imports the User class and creates the database used to store login details
    
    login_manager=LoginManager()
    login_manager.login_view ='auth.login'
    login_manager.init_app(app)
    
    admin =Admin(app) #creates an instance of Admin 
    admin_login=LoginManager()
    
    admin.add_view(ModelView(User, db.session))

    @login_manager.user_loader
    def load_user(id):
        "function that will query the user and load them"
        return User.query.get(int(id))

    return app

def create_database(app):
    "A function that creates the database if it's not been created already"
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
