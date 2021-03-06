"""
This is a admin module called by app.py
"""
from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from typing import List, Dict, Optional

from db import db
from models.user import User
from models.permission import Permission
from models.todo_list import TodoList

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    if current_user.admin:
        if request.method == 'GET':
            users: List[User] = User.query.all()
            return render_template('admin/users.html',
                title='Flask Index',
                message='Users (admin)',
                users=users,
                user=current_user
            )
        if request.method == 'POST':
            # TODO: implement here.
            pass
    else:
        return redirect('/forbidden_access')

@admin_bp.route('/todolists', methods=['GET', 'POST'])
@login_required
def todolists():
    if current_user.admin:
        if request.method == 'GET':
            todolists: List[TodoList] = TodoList.query.all()
            return render_template('admin/todolists.html',
                title='Flask Index',
                message='TodoLists (admin)',
                todolists=todolists,
                user=current_user
            )
        if request.method == 'POST':
            # TODO: implement here.
            pass
    else:
        return redirect('/forbidden_access')

@admin_bp.route('/create_todolist', methods=['GET', 'POST'])
@login_required
def create_todolist():
    if current_user.admin:
        if request.method == 'GET':
            return render_template('user/create_todolist.html',
            title='Flask MySQL',
            message='Create TodoList',
            user=current_user
        )
        if request.method == 'POST':
            listname: str = request.form.get('listname')
            todolist = TodoList(listname=listname)
            db.session.add(todolist)
            db.session.commit()
            return redirect('/admin/todolists')
    else:
        return redirect('/forbidden_access')

@admin_bp.route('/permission', methods=['GET', 'POST'])
@login_required
def permission():
    if current_user.admin:
        if request.method == 'GET':
            permission: List[Permission] = Permission.query.all()
            return render_template('admin/permission.html',
                title='Flask Index',
                message='TodoLists (admin)',
                permissions=permission,
                user=current_user
            )
        if request.method == 'POST':
            # TODO: implement here.
            pass
    else:
        return redirect('/forbidden_access')


@admin_bp.route('/create_permission', methods=['GET', 'POST'])
@login_required
def create_permission():
    if current_user.admin:
        if request.method == 'GET':
            permission: List[Permission] = Permission.query.all()
            users: List[User] = User.query.all()
            todolists: List[TodoList] = TodoList.query.all()
            return render_template('admin/create_permission.html',
                title='Flask MySQL',
                message='Create Permission',
                user=current_user,
                users=users,
                todolists=todolists,
                permissions=permission
            )
        if request.method == 'POST':
            user_id = int(request.form.get('user_id'))
            todolist_id = int(request.form.get('todolist_id'))
            permission = Permission(user_id=user_id, todolist_id=todolist_id)
            db.session.add(permission)
            db.session.commit()
            return redirect('/admin/permission')
    else:
        return redirect('/forbidden_access')