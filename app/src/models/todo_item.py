from db import db
from datetime import datetime
import pytz

class TodoItem(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    taskname = db.Column(db.String(30))
    status = db.Column(db.String(30))
    detail = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, nullable=False,
                    default=datetime.now(pytz.timezone('Asia/Tokyo')))
    todolist_id = db.Column(db.Integer, db.ForeignKey('todo_list.todolist_id'), primary_key=True)
