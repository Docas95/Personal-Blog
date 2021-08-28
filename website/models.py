# file that stores the models for the database
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#defining the schemas for the objects that can be stored in the database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(20))
    username = db.Column(db.String(20), unique=True)
    posts = db.relationship('Post')
    comments = db.relationship('Comment')

class Post(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     title = db.Column(db.String(100))
     data = db.Column(db.String(10000))
     date = db.Column(db.DateTime(timezone=True), default=func.now())
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
     posts = db.relationship('Comment')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_name = db.Column(db.String(100), db.ForeignKey('user.username'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
