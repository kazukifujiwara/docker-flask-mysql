from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os


from db import db
from models.user import User
from models.post import Post
from models.todo_list import TodoList
from models.permission import Permission
from models.todo_item import TodoItem

# import blueprints
from view.admin import admin_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{user}:{password}@{host}/{dbname}?charset=utf8'.format(**{
    'user': 'root',
    'password': 'root',
    'host': 'app_mysql',
    'dbname': 'testdb'
})
app.config['SECRET_KEY'] =  os.urandom(24)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

app.register_blueprint(admin_bp)

# import user's information
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    username = current_user.username
    if request.method == 'GET':
        posts = Post.query.all()
    return render_template('index.html',
        title='Flask Index',
        message=f'Hello, {username}.',
        posts=posts,
        user=current_user
    )

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User(username=username, password=generate_password_hash(password, method='sha256')) 
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    else:
        return render_template('signup.html',
            title='Flask MySQL',
            message='Sign Up'
        )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        #use the first result if there is username's dupurication
        user = User.query.filter_by(username=username).first()

        # TODO: implement if username is not found.

        if check_password_hash(user.password, password):
            login_user(user)
        
        return redirect('/')
    else:
        return render_template('login.html',
            title='Flask MySQL',
            message='Sign In'
        )

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route('/edit_user', methods=['GET', 'POST'])
def edit_user():
    if request.method == 'GET':
        # user = User.query.filter_by(username=username).first()
        return render_template('edit_user.html',
            title='Edit User',
            message=f'Edit user: {current_user.username}',
            user=current_user
        )
    else:
        user = User.query.filter_by(username=current_user.username).first()
        password = request.form.get('password')
        user.password = generate_password_hash(password, method='sha256')
        db.session.commit()
        return redirect('/')

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        post = Post(title=title, body=body)
        db.session.add(post)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('create.html',
            title='Flask MySQL',
            message='register',
            user=current_user
        )

@app.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    post = Post.query.get(id)
    if request.method == 'GET':
        return render_template('update.html',
            title='Flask MySQL',
            message='register',
            post=post,
            user=current_user
        )
    else:
        post.title = request.form.get('title')
        post.body = request.form.get('body')
        db.session.commit()
        return redirect('/')

@app.route('/<int:id>/delete', methods=['GET'])
@login_required
def delete(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/')

# @app.route('/admin/users', methods=['GET', 'POST'])
# @login_required
# def users():
#     # TODO: check admin flag in userdb
#     if current_user.admin:
#         if request.method == 'GET':
#             users = User.query.all()
#             return render_template('users.html',
#                 title='Flask Index',
#                 message='Users (admin)',
#                 users=users,
#                 user=current_user
#             )
#         if request.method == 'POST':
#             # TODO: implement here.
#             pass
#     else:
#         return redirect('/forbidden_access')

@app.route('/forbidden_access', methods=['GET'])
def forbidden_access():
    if request.method == 'GET':
        return render_template('forbidden_access.html',
            title='Flask Index',
            message='',
            user=current_user
        )

# Main function is called only when executing ”python app.py”
if __name__ == '__main__':
   app.debug = True
   app.run(host='0.0.0.0', port=80)