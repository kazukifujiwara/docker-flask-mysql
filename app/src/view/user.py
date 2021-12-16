"""
This is a admin module called by app.py
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
            return render_template('user/user.html',
                title='Flask Index',
                message=f'User: {user.id}',
                user=current_user,
                userinfo = user
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
    