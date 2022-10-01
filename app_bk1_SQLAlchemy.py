from flask import Flask
from flask import render_template, request
from flask_login import LoginManager, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

app.config['MYSQL_HOST'] = 'migae5o25m2psr4q.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'vhqskbgmu3qpnyqa'
app.config['MYSQL_PASSWORD'] = 'peh1p64ucikdulzs'
app.config['MYSQL_DB'] = 'tevm7fxnw6cl3fyr'
 
mysql = MySQL(app)

login_manager = LoginManager() # Login manager for flask-login # New
login_manager.init_app(app) # New

#class Course(db.Model):
#   """Create this course table to store course details"""


# # User.query.all()
# # User.query.filter_by(username="James").first()
# class User(db.Model):
#     """Create columns to store our data"""
 
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(60), unique=True, nullable=False)
#     password = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(60), unique=True, nullable=False)
 
#     def __repr__(self):
#         return '<User %r>' % self.username

#db = SQLAlchemy(app)
#mysql = MySQL(app)

class User(db.Model):
    user_id = db.Column('user_id', db.Integer, primary_key = True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(50))  
    email = db.Column(db.String(200))

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

# New 
# สร้างฟังก์ชันload_user สำหรับโหลดผู้ใช้จาก ID 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def hello_world():
    #return 'Hello, world!'
    return render_template("index.html")

@app.route('/person')
@login_required # New
def person():
    return render_template("person.html")

@app.route('/about')
@login_required # New
def about():
    return render_template("about.html")

@app.route('/sign_up')
def sign_up():
    # Do nothing, only render HTML now
    return render_template("sign_up.html")

# @app.route('/login') # Default is "GET" method
@app.route('/login', methods=['GET', 'POST']) #New --> add "POST"
def login():
    # Do nothing, only render HTML now
    return render_template("login.html")


@app.route('/logout')
def logout():
    # Do nothing, only render HTML now
    return render_template("logout.html")