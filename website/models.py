from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_admin.contrib.sqla import ModelView


class User(db.Model, UserMixin):
    "Class which initiates the values of a new record of a user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150))
    username =db.Column(db.String(15), unique=True)
    password = db.Column(db.String(10))

class AdminModelView(ModelView):
    "Creates the admin view"
    def is_accessible(self):
        return False