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
from view.user import user_bp
from view.todolist import todolist_bp

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

# register blueprints
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)
app.register_blueprint(todolist_bp)

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

    r = db.session.query(Permission.user_id, Permission.todolist_id, TodoList.listname)\
            .filter(Permission.user_id == current_user.id)\
            .outerjoin(TodoList, Permission.todolist_id == TodoList.todolist_id).all()

    if request.method == 'GET':
        posts = Post.query.all()
        return render_template('index.html',
            title='Flask Index',
            message=f'Hello, {current_user.username}.',
            posts=posts,
            user=current_user,
            todolists=r
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