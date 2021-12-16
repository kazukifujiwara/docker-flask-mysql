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

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/<id>', methods=['GET', 'POST'])
@login_required
def user(id):
    if int(id) == current_user.id:
        if request.method == 'GET':
            user = User.query.get(id)
            r = db.session.query(Permission.user_id, Permission.todolist_id, TodoList.listname)\
                    .filter(Permission.user_id == int(id))\
                    .outerjoin(TodoList, Permission.todolist_id == TodoList.todolist_id).all()

            return render_template('user/user.html',
                title='Flask Index',
                message=f'User: {user.id}',
                user=current_user,
                userinfo = user,
                accessible_todolists = r
            )
        if request.method == 'POST':
            # TODO: implement here.
            pass
    else:
        return redirect('/forbidden_access')

@user_bp.route('/<id>/update', methods=['GET', 'POST'])
def update(id):
    if int(id) == current_user.id:
        if request.method == 'GET':
            # user = User.query.filter_by(username=username).first()
            return render_template('user/update.html',
                title='Update User Settings',
                message=f'Update User: {current_user.username}',
                user=current_user
            )
        else:
            user = User.query.filter_by(username=current_user.username).first()
            password = request.form.get('password')
            user.password = generate_password_hash(password, method='sha256')
            db.session.commit()
            return redirect('/')
    else:
        return redirect('/forbidden_access')

@user_bp.route('/<id>/create_todolist', methods=['GET', 'POST'])
@login_required
def create_todolist(id):
    if int(id) == current_user.id:
        if request.method == 'GET':
            return render_template('user/create_todolist.html',
            title='Flask MySQL',
            message='Create TodoList',
            user=current_user
        )
        if request.method == 'POST':
            listname = request.form.get('listname')

            # create todolist
            todolist = TodoList(listname=listname)
            db.session.add(todolist)
            db.session.commit()

            # create permission
            todolist = TodoList.query.filter_by(listname=listname).first()            
            permission = Permission(user_id=id, todolist_id=todolist.todolist_id)
            db.session.add(permission)
            db.session.commit()

            return redirect('/')
    else:
        return redirect('/forbidden_access')