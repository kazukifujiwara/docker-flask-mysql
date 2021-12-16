from db import db

class Permission(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    todolist_id = db.Column(db.Integer, db.ForeignKey('todo_list.todolist_id'), primary_key=True)