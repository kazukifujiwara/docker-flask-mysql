from db import db

class TodoList(db.Model):
    todolist_id = db.Column(db.Integer, primary_key=True)
    listname = db.Column(db.String(30), unique=True)