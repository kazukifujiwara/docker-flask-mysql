"""
This is a user module called by app.py
"""
from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from db import db
from models.user import User
from models.permission import Permission
from models.todo_list import TodoList

todolist_bp = Blueprint('todolist', __name__, url_prefix='/todolist')

@todolist_bp.route('/<id>', methods=['GET', 'POST'])
@login_required
def todolist(id):
    permission = Permission.query.get({
        "user_id": current_user.id,
        "todolist_id": int(id)
    })
    if permission != None:
        todolist = TodoList.query.get(id)
        return render_template('todolist/todolist.html',
                title='Flask Index',
                message='TodoList',
                user=current_user,
                todolist=todolist
            )
    else:
        return redirect('/forbidden_access')
 
