from db import db
from datetime import datetime
from flask import jsonify, abort, request
from flask_login import UserMixin
from flask_restful import Resource

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean, default=False, nullable=False)
