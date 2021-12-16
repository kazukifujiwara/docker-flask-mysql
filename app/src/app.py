from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{user}:{password}@{host}/{dbname}?charset=utf8'.format(**{
    'user': 'root',
    'password': 'root',
    'host': 'app_mysql',
    'dbname': 'testdb'
})
app.config['SECRET_KEY'] =  os.urandom(24)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                    default=datetime.now(pytz.timezone('Asia/Tokyo')))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean, default=False, nullable=False)

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
            message='register'
        )

@app.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    post = Post.query.get(id)
    if request.method == 'GET':
        return render_template('update.html',
            title='Flask MySQL',
            message='register',
            post=post
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

@app.route('/admin/users', methods=['GET', 'POST'])
@login_required
def users():
    # TODO: check admin flag in userdb
    if current_user.admin:
        if request.method == 'GET':
            users = User.query.all()
            return render_template('users.html',
                title='Flask Index',
                message='Users (admin)',
                users=users
            )
        if request.method == 'POST':
            # TODO: implement here.
            pass
    else:
        return redirect('/forbidden_access')

@app.route('/forbidden_access', methods=['GET'])
def forbidden_access():
    if request.method == 'GET':
        return render_template('forbidden_access.html',
            title='Flask Index',
            message=''
        )

# Main function is called only when executing ”python app.py”
if __name__ == '__main__':
   app.debug = True
   app.run(host='0.0.0.0', port=80)